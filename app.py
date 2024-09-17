from PyQt5.QtWidgets import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 700)
        self.setWindowTitle("Aquatic Weeds Predictive System")


if __name__ == "__main__":
    app = QApplication([])
    main_win = App()
    main_win.show()
    app.exec()
