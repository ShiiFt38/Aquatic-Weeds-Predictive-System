from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class Interface():
    def __init__(self, stack):
        self.stack = stack
        self.styles = {
            "primary_btn": """QPushButton {
                                    background-color: #000000; 
                                    color: #ffffff; 
                                    font-family: Helvetica;
                                    font-size: 12px; 
                                    font-weight: bold;
                                    border-radius: 10px;
                                    }
                                    
                                    QPushButton:hover{
                                    background-color: #C1FACA;
                                    color: #000000;
                                    }""",
            "secondary_btn": """QPushButton {
                                    color: #ffffff; 
                                    font-size: 12px; 
                                    font-weight: bold;
                                    border-radius: 10px;
                                    }
                                    
                                    QPushButton:hover{
                                    background-color: #C1FACA;
                                    color: #000000;
                                    }""",
            "tertiary_btn": """QPushButton {
                                            background-color: #000000;
                                            color: #ffffff; 
                                            font-size: 12px; 
                                            font-weight: bold;
                                            border-radius: 10px;
                                            }

                                            QPushButton:hover{
                                            background-color: #C1FACA;
                                            color: #000000;
                                            }""",
            "title_style": """ QLabel {
                                    font-size: 24px; 
                                    font-weight: bold; 
                                    }""",
            "heading_style": """ QLabel {
                                    font-size: 12px; 
                                    font-weight: bold; 
                                    }""",
            "section_style": """
            QGroupBox {
                padding: 50px 50px 50px 50px;
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
        }

        self.calendar_styles = """
                            QCalendarWidget QToolButton {
                                background-color: #6D31ED;
                                color: #E2E2E2;
                                font-size: 16px;
                                height: 30px;
                                width: 100px;
                                icon-size: 20px;
                                font-weight: bold;
                            }
                            QCalendarWidget QToolButton:hover {
                                background-color: #C1FACA;
                                color: #000000;
                            }
                            QCalendarWidget QToolButton:pressed {
                                background-color: #FFBBAA;
                            }
                            QCalendarWidget QMenu {
                                background-color: #333;
                                color: #FFF;
                            }
                            QCalendarWidget QSpinBox {
                                width: 100px;
                                font-size: 14px;
                            }
                            QCalendarWidget QSpinBox::up-button {
                                subcontrol-origin: border;
                                subcontrol-position: top right;
                                width: 30px;
                            }
                            QCalendarWidget QSpinBox::down-button {
                                subcontrol-origin: border;
                                subcontrol-position: bottom right;
                                width: 30px;
                            }
                            QCalendarWidget QWidget#qt_calendar_navigationbar { /* Navigation bar */
                                background-color: #6D31ED;
                            }
                            QCalendarWidget QAbstractItemView:enabled {
                                font-size: 16px;
                                color: #333;
                                background-color: #FFF;
                                selection-background-color: #FFDDC1;
                                selection-color: black;
                            }
                            QCalendarWidget QAbstractItemView:disabled {
                                color: #999;
                            }
                            QCalendarWidget QAbstractItemView:selected {
                                background-color: #FFA07A;
                                color: white;
                            }
                            QCalendarWidget QAbstractItemView:hover {
                                background-color: #FFDDC1;
                                color: #333;
                            }
                        """

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

    def create_tertiary_btn(self, text):
        button = QPushButton(text)
        button.setStyleSheet(self.styles["tertiary_btn"])
        button.setFixedSize(160, 25)
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
        user_widget.setStyleSheet("background-color: #6D31ED; border-radius: 10px;")

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

        sidebar_widget.setStyleSheet("background-color: #00710D; border-radius: 10px")

        # Side menu > User profile contents
        user_layout.addWidget(user_avatar)
        user_info.addWidget(self.create_heading("John Doe"), alignment=Qt.AlignCenter)
        user_info.addWidget(QLabel("View Profile"), alignment=Qt.AlignCenter)
        user_layout.addLayout(user_info)
        # sidebar_layout.addWidget(user_widget)

        # Lambda functions - anonymous functions
        btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_predictions.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_reports.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_data.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        btn_help.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        btn_about.clicked.connect(lambda: self.stack.setCurrentIndex(6))

        return sidebar_widget

    def create_header(self):
        lbl_name = QLabel("AWPS")
        lbl_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #000000;")
        lbl_name.setAlignment(Qt.AlignCenter)

        header_widget = QWidget()

        header_layout = QHBoxLayout(header_widget)

        btn_settings = self.create_primary_btn("Settings")
        btn_logout = self.create_primary_btn("Exit")

        header_layout.addSpacing(50)
        header_layout.addWidget(lbl_name)
        header_layout.addStretch()
        header_layout.addWidget(btn_settings)
        header_layout.addWidget(btn_logout)

        btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(7))
        btn_logout.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        return header_widget

    def create_card_widget(self, title, description, button_text, image_path, button_action = None):
        widget = QGroupBox(title)
        widget.setMinimumSize(250, 250)
        widget.setStyleSheet("""
            QGroupBox {
                padding: 20px 20px 20px 10px;
                border: 1px solid black;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 10px;
                }
        """)
        layout = QVBoxLayout(widget)
        lbl_description = QLabel(description)
        lbl_description.setFont(QFont("Helvetica", 8))
        layout.addWidget(lbl_description, alignment=Qt.AlignCenter)
        lbl_image = QLabel("")
        lbl_image.setPixmap(QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(lbl_image, alignment=Qt.AlignCenter)
        layout.addSpacing(5)
        btn = self.create_tertiary_btn(button_text)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

        if button_action != None:
            btn.clicked.connect(button_action)

        return widget