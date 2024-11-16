from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt, pyqtSignal


class LoadingScreen(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        # Loading gif label
        self.label_animation = QLabel()
        self.movie = QMovie("Assets/Images/Untitled design.gif")  # Create a loading.gif file
        self.label_animation.setMovie(self.movie)

        # Loading text
        self.label_text = QLabel("Loading AWPS...")
        self.label_text.setAlignment(Qt.AlignCenter)
        self.label_text.setStyleSheet("""
            QLabel {
                    font-size: 32px; 
                    font-weight: bold; 
                    color: #6D31ED
                    }
        """)

        layout.addWidget(self.label_animation, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_text, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # Center the loading screen
        self.center_on_screen()

    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def start_animation(self):
        self.movie.start()

    def stop_animation(self):
        self.movie.stop()
        self.close()