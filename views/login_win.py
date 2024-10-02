from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QBrush, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from views.ui import Interface

class Login(QWidget):
    login_successful = pyqtSignal()

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Login - Aquatic Weeds Predictive System")

        ui = Interface(self.stack)

        # Objects
        lbl_title = QLabel("Aquatic Weeds Predictive System")
        logo = QLabel()
        logo.setPixmap(QIcon("Assets/Images/Logo.png").pixmap(64, 64))

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText('Email')
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Password")
        forgot_password = QLabel("Forgot password?")
        btn_login = ui.create_primary_btn("Login")
        lbl_signup = QLabel("Don't have an account? Sign up")

        # Layout
        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()

        main_layout.addWidget(logo, alignment=Qt.AlignCenter)
        main_layout.addWidget(lbl_title, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        form_layout.addWidget(self.txt_email, alignment=Qt.AlignCenter)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.txt_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(forgot_password, alignment=Qt.AlignCenter)
        form_layout.addSpacing(30)
        form_layout.addWidget(btn_login, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_signup, alignment=Qt.AlignCenter)
        form_layout.addStretch()

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet(" color: black; margin-inline: auto;font-weight: bold;")

        lbl_title.setFont(QFont('Helvetica', 24))
        lbl_signup.setFont(QFont('Helvetica', 8))

        self.txt_email.setFixedSize(250, 30)
        self.txt_password.setFixedSize(250, 30)

        self.setAutoFillBackground(True)
        self.home_palette = self.palette()
        self.background_image = QPixmap("Assets/Images/Leaf_bg.png")
        self.update_background(self)

        # Functions
        btn_login.clicked.connect(self.handle_login)

    def update_background(self, view):
        # Calculate the centered rectangle for the background image
        view_rect = view.rect()
        image_rect = self.background_image.rect()

        centered_rect = QRect(
            view_rect.center().x() - image_rect.width() // 2,
            view_rect.center().y() - image_rect.height() // 2,
            image_rect.width(),
            image_rect.height()
        )

        # Create a new pixmap with the size of the view
        centered_pixmap = QPixmap(view_rect.size())
        centered_pixmap.fill(Qt.transparent)

         # Paint the background image onto the new pixmap at the calculated position
        painter = QPainter(centered_pixmap)
        painter.drawPixmap(centered_rect, self.background_image)
        painter.end()

        # Set the centered pixmap as the background
        self.home_palette.setBrush(QPalette.Window, QBrush(centered_pixmap))
        view.setPalette(self.home_palette)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update background image when window is resized
        home_view = self.stack.widget(0)
        self.update_background(home_view)

    def handle_login(self):
        self.login_successful.emit()
