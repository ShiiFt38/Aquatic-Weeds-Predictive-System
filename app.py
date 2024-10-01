from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *
from views.login_win import Login
from views.dashboard_win import Dashboard
from views.predictions_win import Prediction
from views.reports_win import Report
from views.data_win import Data
from views.help_win import Help
from views.about_win import About

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setWindowTitle("Aquatic Weeds Predictive System")
        self.setWindowIcon(QIcon("Assets/Images/Logo.png"))


        self.stack = QStackedWidget()

        self.login_widget = Login(self.stack)
        self.dashboard_widget = Dashboard(self.stack)
        self.predictions = Prediction(self.stack)
        self.reports = Report(self.stack)
        self.data = Data(self.stack)
        self.help = Help(self.stack)
        self.about = About(self.stack)

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.addWidget(self.predictions)
        self.stack.addWidget(self.reports)
        self.stack.addWidget(self.data)
        self.stack.addWidget(self.help)
        self.stack.addWidget(self.about)

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
