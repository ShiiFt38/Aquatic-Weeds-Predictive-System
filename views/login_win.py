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
        lbl_email = QLabel("Email")
        lbl_password = QLabel("Password")
        lbl_forgot_password = QLabel("Forgot password?")
        btn_login = ui.create_primary_btn("Login")
        lbl_signup = QLabel("Don't have an account? Sign up")

        # Layout
        form_widget = QWidget()

        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout(form_widget)

        main_layout.addWidget(logo, alignment=Qt.AlignCenter)
        main_layout.addWidget(lbl_title, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        form_layout.addWidget(lbl_email)
        form_layout.addWidget(self.txt_email, alignment=Qt.AlignCenter)
        form_layout.addSpacing(20)
        form_layout.addWidget(lbl_password)
        form_layout.addWidget(self.txt_password, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_forgot_password, alignment=Qt.AlignCenter)
        form_layout.addSpacing(30)
        form_layout.addWidget(btn_login, alignment=Qt.AlignCenter)
        form_layout.addWidget(lbl_signup, alignment=Qt.AlignCenter)
        form_layout.addStretch()
        form_widget.setLayout(form_layout)

        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet(" color: black; font-weight: bold;")

        lbl_title.setFont(QFont('Helvetica', 24))
        lbl_signup.setFont(QFont('Helvetica', 8))

        lineedit_styles = """
            QLineEdit {
                background-color: white;
                color: white;
                padding: 5px;
                border-radius: 10px;
            }
            QLineEdit::placeholder {
                color: black;
            }
        """

        self.txt_email.setStyleSheet(lineedit_styles)
        self.txt_password.setStyleSheet(lineedit_styles)
        self.txt_email.setFixedSize(250, 30)
        self.txt_password.setFixedSize(250, 30)

        label_styles = "background: transparent; color: white; font-weight: bold;"
        lbl_email.setStyleSheet(label_styles)
        lbl_email.setFont(QFont("Helvetica"))
        lbl_password.setStyleSheet(label_styles)
        lbl_email.setFont(QFont("Helvetica"))
        lbl_forgot_password.setStyleSheet(label_styles)
        lbl_signup.setStyleSheet(label_styles)

        self.setAutoFillBackground(True)
        self.home_palette = self.palette()
        self.background_image = QPixmap("Assets/Images/Leaf_bg.png")
        self.update_background(self)

        form_widget.setStyleSheet("background-color: rgba(0, 0, 0, 128); border-radius: 10px;")
        form_widget.setContentsMargins(100, 40, 100, 60)

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
