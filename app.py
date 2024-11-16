from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import QTimer
from models.db import VegetationDatabase
from views.loading_screen import LoadingScreen

class App(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize loading screen
        self.loading_screen = LoadingScreen()
        self.loading_screen.show()
        self.loading_screen.start_animation()

        # Use timer to simulate loading and initialize components
        QTimer.singleShot(100, self.initialize_app)

    def initialize_app(self):
        # Initialize main application
        self.setMinimumSize(1100, 600)
        self.setWindowTitle("Aquatic Weeds Predictive System")
        self.setWindowIcon(QIcon("Assets/Images/Logo.png"))

        self.stack = QStackedWidget(self)
        self.db = VegetationDatabase()

        # Initialize all widgets
        self.init_widgets()

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.login_widget.login_successful.connect(self.switch_to_dashboard)

        # Close loading screen and show main window
        QTimer.singleShot(2000, self.finish_loading)  # Adjust delay as needed

    def init_widgets(self):
        from views.login_win import Login
        from views.dashboard_win import Dashboard
        from views.predictions_win import Prediction
        from views.reports_win import Report
        from views.data_win import Data
        from views.help_win import Help
        from views.about_win import About
        from views.settings_win import Settings

        self.login_widget = Login(self.stack)
        self.dashboard_widget = Dashboard(self.stack, self.db)
        self.predictions = Prediction(self.stack, self.db)
        self.reports = Report(self.stack, self.db)
        self.data = Data(self.stack, self.db)
        self.help = Help(self.stack)
        self.about = About(self.stack)
        self.settings = Settings(self.stack)

        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.dashboard_widget)
        self.stack.addWidget(self.predictions)
        self.stack.addWidget(self.reports)
        self.stack.addWidget(self.data)
        self.stack.addWidget(self.help)
        self.stack.addWidget(self.about)
        self.stack.addWidget(self.settings)

    def finish_loading(self):
        self.loading_screen.stop_animation()
        self.show()

    def switch_to_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_widget)


if __name__ == "__main__":
    app = QApplication([])
    main_win = App()
    app.exec()