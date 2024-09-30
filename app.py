from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from views.login_win import Login
from views.dashboard_win import Dashboard

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle("Aquatic Weeds Predictive System")
        self.setWindowIcon(QIcon("Assets/Images/Logo.png"))


        self.stack = QStackedWidget()

        self.login_widget = Login()
        self.dashboard_widget = Dashboard()

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.dashboard_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.login_widget.login_successful.connect(self.switch_to_dashboard)

    def switch_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_widget)



if __name__ == "__main__":
    app = QApplication([])
    main_win = App()
    main_win.show()
    app.exec()
