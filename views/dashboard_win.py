from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Objects
        lbl_name = QLabel("AWPS")

        btn_dashboard = QPushButton("Dashboard")
        btn_predictions = QPushButton("Predictions")
        btn_reports = QPushButton("Reports")
        btn_data = QPushButton("Data Management")

        btn_help = QPushButton("Help and Support")
        btn_about = QPushButton("About")
        btn_settings = QPushButton("Settings")

        user_avatar = QLabel()
        user_avatar.setPixmap(QPixmap("Assets/Images/Logo.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        lbl_welcome = QLabel("Welcome to your Dashboard")


        # Layout
        content_widget = QWidget()
        user_widget = QWidget()

        main_layout = QHBoxLayout()
        header_layout = QHBoxLayout()
        content_area = QScrollArea()
        content_layout = QVBoxLayout(content_widget)
        sidebar_layout = QVBoxLayout()
        user_layout = QHBoxLayout(user_widget)
        user_info = QVBoxLayout()

        self.setLayout(main_layout)

        # sidebar contents
        sidebar_layout.addWidget(lbl_name)
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_predictions)
        sidebar_layout.addWidget(btn_reports)
        sidebar_layout.addWidget(btn_data)
        sidebar_layout.addWidget(btn_help)
        sidebar_layout.addWidget(btn_about)
        sidebar_layout.addWidget(btn_settings)

        # Side menu > User profile contents
        user_layout.addWidget(user_avatar)
        user_info.addWidget(QLabel("John Doe"))
        user_info.addWidget(QLabel("View Profile"))
        user_layout.addLayout(user_info)
        sidebar_layout.addWidget(user_widget)

        # Content layout
        content_layout.addWidget(lbl_welcome)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)

        main_layout.addLayout(sidebar_layout)
        main_layout.addWidget(content_area, 1)

        # Design
        sidebar_layout.addStretch()

        lbl_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a4a4a; margin-bottom: 24px")
        lbl_name.setAlignment(Qt.AlignCenter)

        # Iterate through side menu widgets and creates button widgets list
        buttons = []
        for i in range(sidebar_layout.count()):
            widget = sidebar_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                buttons.append(widget)

        for button in buttons:
            button.setStyleSheet("""QPushButton {
                                    color: #000000; 
                                    font-size: 12px; 
                                    font-weight: bold;
                                    border-radius: 10px;}
                                    
                                    QPushButton:hover{
                                    background-color: #C1FACA;
                                    color: #00710D;
                                    }
                                    """)
            button.setFixedSize(140, 35)

        lbl_welcome.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")

        # Functions
