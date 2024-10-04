import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QPixmap, QImage
from views.ui import Interface
from controllers.image_processor import ImageProcessor


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

        lbl_summary = ui.create_heading("Prediction Model")

        lbl_image_type = ui.create_heading("Original Image")
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
        btn_upload = ui.create_tertiary_btn("Upload")

        lbl_prediction_title = ui.create_heading("Prediction")
        lbl_prediction_image = QLabel("Upload Image to Generate")
        btn_prediction = ui.create_tertiary_btn("Generate")

        txt_chat_entry = QLineEdit()
        txt_chat_entry.setPlaceholderText('Enter prompt here')
        btn_chat = QPushButton("Send")

        # Layout
        content_widget = QWidget()
        upload_widget = QWidget()
        prediction_widget = QWidget()
        chat_widget = QWidget()

        content_area = QScrollArea()
        chat_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QVBoxLayout(content_widget)
        column_area = QHBoxLayout()
        first_column = QVBoxLayout()
        second_column = QVBoxLayout()
        global images_layout
        images_layout = QStackedLayout()
        button_layout = QHBoxLayout()
        actions_layout = QHBoxLayout()
        upload_layout = QVBoxLayout(upload_widget)
        prediction_layout = QVBoxLayout(prediction_widget)
        chat_layout = QVBoxLayout(chat_widget)
        prompt_area = QHBoxLayout()

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

        # Content layout > First column > First row
        first_column.addWidget(QLabel("Original Image:"))
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

        # Content layout > second column
        second_column.addWidget(lbl_summary, alignment=Qt.AlignCenter)
        second_column.addWidget(chat_area)
        chat_area.setWidget(chat_widget)
        chat_area.setWidgetResizable(True)
        chat_layout.addStretch()
        chat_layout.addLayout(prompt_area)

        prompt_area.addWidget(txt_chat_entry)
        prompt_area.addWidget(btn_chat)

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

        chat_widget.setMaximumSize(400, 600)
        chat_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        txt_chat_entry.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        txt_chat_entry.setMinimumHeight(30)
        btn_chat.setStyleSheet("""QPushButton {
                                            background-color: #000000;
                                            color: #ffffff; 
                                            font-size: 12px; 
                                            font-weight: bold;
                                            border-radius: 10px;
                                            }

                                            QPushButton:hover{
                                            background-color: #C1FACA;
                                            color: #000000;
                                            }""")
        btn_chat.setFixedSize(60, 25)

        # Functions
        for _ in range(3):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setPixmap(QPixmap("Assets/Images/undraw_void_3ggu.png").scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            images_layout.addWidget(label)

        btn_original.clicked.connect(lambda: images_layout.setCurrentIndex(0))
        btn_enhanced.clicked.connect(lambda: images_layout.setCurrentIndex(1))
        btn_detected.clicked.connect(lambda: images_layout.setCurrentIndex(2))

        btn_upload.clicked.connect(self.handle_image_upload)

    def handle_image_upload(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)")

        if image_path:
            processor = ImageProcessor(image_path)

            pixmap_1 = QPixmap(image_path)
            original_image = images_layout.widget(0)
            original_image.setAlignment(Qt.AlignCenter)
            original_image.setPixmap(pixmap_1.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            enhancement = processor.enhance_green_vegetation()
            rgb_image = cv2.cvtColor(enhancement, cv2.COLOR_BGR2RGB)

            # Get image dimensions
            h, w, ch = rgb_image.shape
            # Convert to QImage
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            pixmap_2 = QPixmap.fromImage(q_img)
            enhanced_image = images_layout.widget(1)
            enhanced_image.setAlignment(Qt.AlignCenter)
            enhanced_image.setPixmap(pixmap_2.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # detected = processor.detect_and_analyze_vegetation(enhancement)
            # rgb_image_2 = cv2.cvtColor(detected, cv2.COLOR_BGR2RGB)
            #
            # # Get image dimensions
            # h, w, ch = rgb_image.shape
            # # Convert to QImage
            # bytes_per_line = ch * w
            # q_img_2 = QImage(rgb_image_2.data, w, h, bytes_per_line, QImage.Format_RGB888)
            # pixmap_3 = QPixmap.fromImage(q_img_2)
            # detected_image = images_layout.widget(2)
            # detected_image.setAlignment(Qt.AlignCenter)
            # detected_image.setPixmap(pixmap_3.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))