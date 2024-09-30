from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class Login(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self.setWindowTitle("Login - Aquatic Weeds Predictive System")

        # Objects
        lbl_title = QLabel("Aquatic Weeds Predictive System")
        logo = QLabel()
        logo.setPixmap(QIcon("Assets/Images/Logo.png").pixmap(64, 64))

        # lbl_intro = QLabel(
        # "Welcome \nGet creative insights and accurate forecasts from a \ntrained and fine-tuned artificial intelligent agent.")
        lbl_email = QLabel("Email:")
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText('Email')
        lbl_password = QLabel("Password:")
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        forgot_password = QLabel("Forgot password?")
        btn_login = QPushButton("Login")
        lbl_signup = QLabel("Don't have an account? Sign up")

        # Layout
        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()

        main_layout.addWidget(logo, alignment=Qt.AlignCenter)
        main_layout.addWidget(lbl_title, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20)

        form_layout.addSpacing(20)
        # form_layout.addWidget(lbl_email, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.txt_email, alignment=Qt.AlignCenter)
        form_layout.addSpacing(20)
        # form_layout.addWidget(lbl_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.txt_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(forgot_password, alignment=Qt.AlignCenter)
        form_layout.addSpacing(30)
        form_layout.addWidget(btn_login, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_signup, alignment=Qt.AlignCenter)
        form_layout.addSpacing(20)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

        # Design
        self.setStyleSheet("""
            QDialog{
                background-image: url('Assets/Images/Leaf_bg.png');
                background-position: cover;
                background-repeat: no-repeat;
                }
        """)

        lbl_title.setStyleSheet(" color: black; margin-inline: auto;font-weight: bold;")

        lbl_title.setFont(QFont('Arial', 24))
        lbl_signup.setFont(QFont('Arial', 8))

        btn_login.setFixedSize(200, 35)
        self.txt_email.setFixedSize(200, 30)
        self.txt_password.setFixedSize(200, 30)

        btn_login.setStyleSheet("""QPushButton {
        background-color: #00710D; 
        color: #000000; 
        font-size: 12px; 
        font-weight: bold;
        border-radius: 10px;}
        
        QPushButton:hover{
        background-color: #C1FACA;
        color: #00710D;
        }
        """)

        # Functions
        btn_login.clicked.connect(self.handle_login)

    def handle_login(self):
        self.login_successful.emit()
