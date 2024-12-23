import cv2
from PyQt5.QtWidgets import (QWidget, QGroupBox, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea,
                             QStackedLayout, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os
from views.ui import Interface
from controllers.image_processor import ImageProcessor
from controllers.weather_handler import WeatherHandler
from controllers.centroid_predictor import PredictionModel
from controllers.gemini_assistant import GeminiAssistant

class Prediction(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.db = db
        self.ui = Interface(self.stack)
        self.prediction_model = PredictionModel(self.db)
        self.gemini_assistant = GeminiAssistant()

        self.image_list = ['Assets/Images/Hartbeespoort_original.jpg', 'Assets/Images/Enhanced_Vegetation.jpg',
                           'Assets/Images/Detected analysis.jpg']

        # Objects
        sidebar = self.ui.create_sidebar()
        header = self.ui.create_header()

        lbl_title = self.ui.create_title("Prediction Tools")

        btn_original = self.ui.create_tertiary_btn("Original")
        btn_enhanced = self.ui.create_tertiary_btn("Enhanced")
        btn_detected = self.ui.create_tertiary_btn("Detected")

        lbl_upload_image = QLabel("Image Display")
        lbl_upload_image.setPixmap(QPixmap("Assets/Images/undraw_Going_up_re_86kg.png").scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lbl_upload_image.setAlignment(Qt.AlignCenter)
        btn_upload = self.ui.create_tertiary_btn("Upload")

        self.lbl_prediction_image = QLabel("Upload Image to Generate")
        btn_prediction = self.ui.create_tertiary_btn("Generate")
        global txt_chat_entry
        txt_chat_entry = QLineEdit()
        txt_chat_entry.setPlaceholderText('Enter prompt here')
        btn_chat = QPushButton("Send")

        # Layout
        content_widget = QWidget()
        upload_widget = QGroupBox("Upload Image")
        prediction_widget = QGroupBox("Prediction")
        chat_widget = QGroupBox("Prediction Model")

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
        prompt_layout = QHBoxLayout()

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
        upload_layout.addSpacing(10)
        upload_layout.addWidget(lbl_upload_image, alignment=Qt.AlignCenter)
        upload_layout.addWidget(btn_upload, alignment=Qt.AlignCenter)

        # Content layout > First column > Prediction card widget
        prediction_layout.setSpacing(5)
        prediction_layout.addWidget(self.lbl_prediction_image, alignment=Qt.AlignCenter)
        prediction_layout.addWidget(btn_prediction, alignment=Qt.AlignCenter)

        # Content layout > second column
        second_column.addWidget(chat_area)
        chat_area.setWidget(chat_widget)
        chat_area.setWidgetResizable(True)
        chat_layout.addStretch()
        chat_layout.addLayout(prompt_layout)

        prompt_layout.addWidget(txt_chat_entry)
        prompt_layout.addWidget(btn_chat)

        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")

        groupbox_styles = """
            QGroupBox {
                border: 1px solid black;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 10px;
                }
        """
        upload_widget.setMinimumSize(250, 250)
        upload_widget.setStyleSheet(groupbox_styles)
        prediction_widget.setMinimumSize(250, 250)
        prediction_widget.setStyleSheet(groupbox_styles)

        chat_widget.setMaximumSize(400, 600)
        chat_widget.setStyleSheet("""
            QGroupBox {
                border: 1px solid black;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                }
        """)
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
        btn_prediction.clicked.connect(self.handle_generate_prediction)

        btn_chat.clicked.connect(self.handle_chat)

    def retrieve_weather_data(self, date):
        weather = WeatherHandler(self.db)

        weather_data = weather.get_historical_weather_data(date)
        weather.print_weather_data(weather_data)

    def handle_image_upload(self):
        print("Uploading Image...")
        file_dialog = QFileDialog(self)
        image_path, _ = file_dialog.getOpenFileName(self, "Select Image",
                                                    "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif)")
        date = image_path[-14:-4]
        if date:
            self.retrieve_weather_data(date)

        print("processing image...")
        if image_path:
            processor = ImageProcessor(image_path, self.db)

            pixmap_1 = QPixmap(image_path)
            original_image = images_layout.widget(0)
            original_image.setAlignment(Qt.AlignCenter)
            original_image.setPixmap(pixmap_1.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            print("Enhancing image...")
            enhancement = processor.enhance_green_vegetation()
            self.handle_image_transformation(enhancement, 1)

            detected, veg_data = processor.detect_and_analyze_vegetation(enhancement, image_path)
            if veg_data == []:
               pixmap = QPixmap("Assets/Images/undraw_Searching_re_3ra9.png")
               detected_image = images_layout.widget(2)
               detected_image.setAlignment(Qt.AlignCenter)
               detected_image.setPixmap(pixmap.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
               self.handle_image_transformation(detected, 2)

    def handle_image_transformation(self, image, widget_index):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Get image dimensions
        h, w, ch = rgb_image.shape
        # Convert to QImage
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        pixmap_2 = QPixmap.fromImage(q_img)
        enhanced_image = images_layout.widget(widget_index)
        enhanced_image.setAlignment(Qt.AlignCenter)
        enhanced_image.setPixmap(pixmap_2.scaled(360, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def handle_generate_prediction(self):
        self.prediction_model.train_model()
        self.prediction_model.predict_and_store()

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT image_path
        FROM image_scans
        ORDER BY time_scanned DESC
        LIMIT 1
    ''')

        result = cursor.fetchone()
        if result:
            image_path = result[0]
            print(f"Image fetched: {image_path}")
        else:
            print("No image found.")
            return

        # Fetch the latest prediction data
        cursor.execute('''
            SELECT predicted_centroid_x, predicted_centroid_y
            FROM vegetation_predictions
            ORDER BY prediction_id DESC
            LIMIT 1
        ''')
        prediction_result = cursor.fetchone()
        if prediction_result:
            predicted_data = [
                {
                    "predicted_centroid_x": prediction_result[0],
                    "predicted_centroid_y": prediction_result[1]
                }
            ]
        else:
            print("No prediction data found.")
            return

        image = cv2.imread(image_path)
        if image is None:
            print("Error loading image.")
            return

        # Initialize ImageProcessor and plot predicted centroids
        processor = ImageProcessor(image_path, self.db)
        image_with_predictions = processor.plot_predicted_centroids(image, predicted_data)

        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder to Save Image")
        if not folder_path:
            print("No folder selected.")
            return

        # Define the full path for saving the image
        save_path = os.path.join(folder_path, "image_with_predictions.png")

        # Save the image with plotted centroids
        cv2.imwrite(save_path, image_with_predictions)
        print(f"Image saved to {save_path}")

        pixmap = QPixmap(save_path)
        self.lbl_prediction_image.setPixmap(pixmap.scaled(240, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def handle_chat(self):
        prompt = txt_chat_entry.text()
        print(f"Prompt: {prompt}")
        self.gemini_assistant.generate_response(prompt)