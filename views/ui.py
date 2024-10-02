from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class Interface():
    def __init__(self, stack):
        self.stack = stack
        self.styles = {
            "primary_btn": """QPushButton {
                                    background-color: #00710D; 
                                    color: #ffffff; 
                                    font-family: Helvetica;
                                    font-size: 12px; 
                                    font-weight: bold;
                                    border-radius: 10px;
                                    cursor: pointer;
                                    transition: background-color 0.3s ease, transform 0.3s ease;}
                                    
                                    QPushButton:hover{
                                    background-color: #C1FACA;
                                    color: #00710D;
                                    }""",
            "secondary_btn": """QPushButton {
                                    color: #000000; 
                                    font-size: 12px; 
                                    font-weight: bold;
                                    border-radius: 10px;
                                    cursor: pointer;
                                    transition: background-color 0.3s ease, transform 0.3s ease;
                                    }
                                    
                                    QPushButton:hover{
                                    background-color: #C1FACA;
                                    color: #00710D;
                                    }""",
            "title_style": """ QLabel {
                                    font-size: 24px; 
                                    font-weight: bold; 
                                    margin: 20px 0;
                                    }""",
            "heading_style": """ QLabel {
                                    font-size: 12px; 
                                    font-weight: bold; 
                                    }"""
        }

    def create_primary_btn(self, text):
        button = QPushButton(text)
        button.setStyleSheet(self.styles["primary_btn"])
        button.setFixedSize(200, 35)
        button.setFont(QFont('Helvetica', 12))

        return button

    def create_secondary_btn(self, text):
        button = QPushButton(text)
        button.setStyleSheet(self.styles["secondary_btn"])
        button.setFixedSize(160, 35)
        button.setFont(QFont('Helvetica', 12))

        return button

    def create_title(self, text):
        lbl_title = QLabel(text)
        lbl_title.setStyleSheet(self.styles["title_style"])
        lbl_title.setFont(QFont('Helvetica', 12))

        return lbl_title

    def create_heading(self, text):
        lbl_heading = QLabel(text)
        lbl_heading.setStyleSheet(self.styles["heading_style"])
        lbl_heading.setFont(QFont('Helvetica', 12))

        return lbl_heading

    def create_sidebar(self):
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(180)
        user_widget = QWidget()

        sidebar_layout = QVBoxLayout(sidebar_widget)
        user_layout = QHBoxLayout(user_widget)
        user_info = QVBoxLayout()

        btn_dashboard = self.create_secondary_btn("Dashboard")
        btn_predictions = self.create_secondary_btn("Predictions")
        btn_reports = self.create_secondary_btn("Reports")
        btn_data = self.create_secondary_btn("Data Management")
        btn_help = self.create_secondary_btn("Help and Support")
        btn_about = self.create_secondary_btn("About")

        user_avatar = QLabel()
        user_avatar.setPixmap(
            QPixmap("Assets/Images/profile.jpg").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        sidebar_layout.addSpacing(10)
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_predictions)
        sidebar_layout.addWidget(btn_reports)
        sidebar_layout.addWidget(btn_data)
        sidebar_layout.addWidget(btn_help)
        sidebar_layout.addWidget(btn_about)
        sidebar_layout.addStretch()

        # Side menu > User profile contents
        user_layout.addWidget(user_avatar)
        user_info.addWidget(QLabel("John Doe"), alignment=Qt.AlignCenter)
        user_info.addWidget(QLabel("View Profile"), alignment=Qt.AlignCenter)
        user_layout.addLayout(user_info)
        sidebar_layout.addWidget(user_widget)

        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_predictions.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_reports.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_data.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        btn_help.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        btn_about.clicked.connect(lambda: self.stack.setCurrentIndex(6))

        return sidebar_widget

    def create_header(self):
        lbl_name = QLabel("AWPS")
        lbl_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #6D31ED; margin-bottom: 24px")
        lbl_name.setAlignment(Qt.AlignCenter)

        header_widget = QWidget()

        header_layout = QHBoxLayout(header_widget)

        btn_settings = self.create_primary_btn("Settings")
        btn_logout = self.create_primary_btn("Log Out")

        header_layout.addSpacing(50)
        header_layout.addWidget(lbl_name)
        header_layout.addStretch()
        header_layout.addWidget(btn_settings)
        header_layout.addWidget(btn_logout)

        btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(7))
        btn_logout.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        return header_widget

    def create_card_widget(self, title, description, button_text, image_path):
        widget = QWidget()
        widget.setMinimumSize(250, 250)
        widget.setStyleSheet("background-color: #E2E2E2; border-radius: 10px;")
        layout = QVBoxLayout(widget)
        lbl_heading = self.create_heading(title)
        layout.addWidget(lbl_heading)
        layout.addSpacing(5)
        lbl_description = QLabel(description)
        lbl_description.setFont(QFont("Helvetica", 8))
        layout.addWidget(lbl_description)
        lbl_image = QLabel("")
        lbl_image.setPixmap(QPixmap(image_path).scaled(132, 132, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(lbl_image, alignment=Qt.AlignCenter)
        layout.addSpacing(5)
        btn = self.create_primary_btn(button_text)
        layout.addWidget(btn, alignment=Qt.AlignCenter)
        return widget