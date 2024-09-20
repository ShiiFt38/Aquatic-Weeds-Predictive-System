from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self.setWindowTitle("Login - Aquatic Weeds Predictive System")

        # Objects
        lbl_title = QLabel("Aquatic Weeds Predictive System")
        logo = QLabel()
        logo.setPixmap(QIcon("Assets/Images/Logo.png").pixmap(64, 64))

        lbl_intro = QLabel("Get creative insights and accurate forecasts from a trained and fine-tuned artificial intelligent agent.")
        lbl_email = QLabel("Email:")
        self.txt_email = QLineEdit()
        lbl_password = QLabel("Password:")
        self.txt_password = QLineEdit()
        forgot_password = QLabel("Forgot password?")
        btn_login = QPushButton("Login")
        lbl_signup = QLabel("Don't have an account? Sign up")


        # Layout
        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()

        main_layout.addWidget(logo, alignment=Qt.AlignCenter)
        main_layout.addWidget(lbl_title, alignment=Qt.AlignCenter)


        form_layout.addWidget(lbl_intro, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_email, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.txt_email, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.txt_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(btn_login, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_signup, alignment=Qt.AlignCenter)

        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)


        # Design
        self.setStyleSheet("""
            QDialog{
                background-image: url('Assets/Images/Leaf_bg.png');
                background-position: center;
                background-repeat: no-repeat;
                }
        """)

        lbl_title.setStyleSheet(" font: 32px black; margin-inline: auto;font-weight: bold; padding-bottom: 200px")

        btn_login.setFixedSize(200, 35)

        btn_login.setStyleSheet(
            "background-color: green; color: white; font-size: 16px; font-weight: bold;"
        )

        #Functions

