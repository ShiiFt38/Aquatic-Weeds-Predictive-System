from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QPixmap
from views.ui import Interface


class Prediction(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        ui = Interface(self.stack)

        self.image_list = ['Assets/Images/Hartbeespoort_original.jpg', 'Assets/Images/Enhanced_Vegetation.jpg',
                           'Assets/Images/Detected analysis.jpg']

        # Objects
        sidebar = ui.create_sidebar()
        header = ui.create_header()

        lbl_title = ui.create_title("Prediction Tools")

        lbl_summary = ui.create_heading("Summary")

        btn_original = ui.create_tertiary_btn("Original")
        btn_enhanced = ui.create_tertiary_btn("Enhanced")
        btn_detected = ui.create_tertiary_btn("Detected")

        lbl_upload_title = ui.create_heading("Upload Image")
        global lbl_upload_image
        lbl_upload_image = QLabel("Image Display")
        pixmap = QPixmap("Assets/Images/undraw_Going_up_re_86kg.png")
        scaled_pixmap = pixmap.scaled(132, 132, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        lbl_upload_image.setPixmap(scaled_pixmap)
        lbl_upload_image.setAlignment(Qt.AlignCenter)
        btn_upload = ui.create_primary_btn("Upload")

        lbl_prediction_title = ui.create_heading("Prediction")
        lbl_prediction_image = QLabel("Upload Image to Generate")
        btn_prediction = ui.create_primary_btn("Generate")

        # Layout
        content_widget = QWidget()
        upload_widget = QWidget()
        prediction_widget = QWidget()

        content_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QVBoxLayout(content_widget)
        column_area = QHBoxLayout()
        first_column = QVBoxLayout()
        second_column = QVBoxLayout()
        images_layout = QStackedLayout()
        button_layout = QHBoxLayout()
        actions_layout = QHBoxLayout()
        upload_layout = QVBoxLayout(upload_widget)
        prediction_layout = QVBoxLayout(prediction_widget)

        # Inner Layout
        inner_layout.addWidget(sidebar)
        inner_layout.addWidget(content_area, 1)

        # Content layout
        content_layout.addWidget(lbl_title)
        content_layout.addLayout(column_area)
        content_widget.setLayout(content_layout)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)

        # Content Layout > column area
        column_area.addLayout(first_column)
        column_area.addLayout(second_column)
        column_area.setStretch(0, 3)
        column_area.setStretch(1, 1)
        second_column.addWidget(lbl_summary, alignment=Qt.AlignCenter)
        second_column.addStretch()

        # Content layout > First column > First row
        first_column.addLayout(images_layout)
        images_layout.setSizeConstraint(30)

        # Content layout > First column > Button layout
        first_column.addLayout(button_layout)
        button_layout.addStretch()
        button_layout.addWidget(btn_original)
        button_layout.addWidget(btn_enhanced)
        button_layout.addWidget(btn_detected)
        button_layout.addStretch()

        # Content layout > First column > Actions layout
        first_column.addSpacing(20)
        first_column.addLayout(actions_layout)
        actions_layout.addWidget(upload_widget)
        actions_layout.addWidget(prediction_widget)

        # Content layout > First column > Upload card widget
        upload_layout.setSpacing(5)
        upload_layout.addWidget(lbl_upload_title, alignment=Qt.AlignCenter)
        upload_layout.addWidget(lbl_upload_image, alignment=Qt.AlignCenter)
        upload_layout.addWidget(btn_upload, alignment=Qt.AlignCenter)

        # Content layout > First column > Prediction card widget
        prediction_layout.setSpacing(5)
        prediction_layout.addWidget(lbl_prediction_title, alignment=Qt.AlignCenter)
        prediction_layout.addWidget(lbl_prediction_image, alignment=Qt.AlignCenter)
        prediction_layout.addWidget(btn_prediction, alignment=Qt.AlignCenter)


        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")

        widget_styles = "background-color: #E2E2E2; border-radius: 10px;"
        upload_widget.setMinimumSize(250, 250)
        upload_widget.setStyleSheet(widget_styles)
        prediction_widget.setMinimumSize(250, 250)
        prediction_widget.setStyleSheet(widget_styles)

        # Functions
        for image_path in self.image_list:
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setPixmap(QPixmap(image_path).scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            images_layout.addWidget(label)

        btn_original.clicked.connect(lambda: images_layout.setCurrentIndex(0))
        btn_enhanced.clicked.connect(lambda: images_layout.setCurrentIndex(1))
        btn_detected.clicked.connect(lambda: images_layout.setCurrentIndex(2))

        btn_upload.clicked.connect(self.handle_image_upload)

    def handle_image_upload(self):
        global selected_image_path
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)")

        if image_path:
            selected_image_path = image_path
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(132, 132, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_upload_image.setPixmap(scaled_pixmap)
            lbl_upload_image.setAlignment(Qt.AlignCenter)
