from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from views.login_dialog import Login
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle("Aquatic Weeds Predictive System")
        self.setWindowIcon(QIcon("Assets/Images/Logo.png"))
        self.display_login()

    def display_login(self):
        login_dialog = Login()

        login_dialog.exec()


if __name__ == "__main__":
    app = QApplication([])
    main_win = App()
    app.exec()
