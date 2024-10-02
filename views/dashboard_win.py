from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from views.ui import Interface

class Dashboard(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Interface(self.stack)

        # Objects
        sidebar = self.ui.create_sidebar()
        header = self.ui.create_header()

        lbl_welcome = QLabel("Welcome to your Dashboard")

        # Layout
        content_widget = QWidget()

        content_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QVBoxLayout(content_widget)
        first_row = QHBoxLayout()
        second_row = QHBoxLayout()
        third_row = QHBoxLayout()


        # Inner Layout
        inner_layout.addWidget(sidebar)
        inner_layout.addWidget(content_area, 1)

        # Content layout
        content_layout.addWidget(lbl_welcome)
        content_layout.addLayout(first_row)
        content_layout.addLayout(second_row)
        content_layout.addLayout(third_row)
        content_layout.addStretch()
        content_layout.setSpacing(20)
        content_widget.setLayout(content_layout)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)
        content_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Content layout > first row
        first_row.addWidget(self.create_prediction_history())
        first_row.addWidget(self.create_new_prediction())
        first_row.addSpacing(30)

        # Content layout > second row
        second_row.addWidget(self.create_current_prediction(), alignment=Qt.AlignCenter)

        # Content layout > third row
        third_row.addStretch()
        third_row.setSpacing(20)
        third_row.addWidget(self.create_compare_predictions())
        third_row.addWidget(self.create_recent_predictions())
        third_row.addWidget(self.create_reports())
        third_row.addStretch()


        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_welcome.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")

    # Functions
    def create_prediction_history(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: #E2E2E2; border-radius: 10px;")
        widget.setMaximumSize(1100, 400)
        layout = QVBoxLayout(widget)
        lbl_heading = self.ui.create_heading("Prediction History")
        layout.addWidget(lbl_heading)

        table = QTableWidget(4, 2)
        table.setHorizontalHeaderLabels(["Date", "Description"])
        for i in range(4):
            table.setItem(i, 0, QTableWidgetItem("2024/07/28"))
            table.setItem(i, 1, QTableWidgetItem(""))
        layout.addWidget(table)

        return widget

    def create_new_prediction(self):
        return self.ui.create_card_widget("New Prediction",
                                       "Enhance image quality with advanced AI. ",
                                       "New", "Assets/Images/Scanned Image.png")

    def create_current_prediction(self):
        widget = QWidget()
        widget.setStyleSheet("background-color: #E2E2E2; border-radius: 10px;")
        widget.setMaximumSize(1500, 400)
        layout = QVBoxLayout(widget)
        lbl_heading = self.ui.create_heading("Current Prediction")
        layout.addWidget(lbl_heading)
        layout.addWidget(QLabel("Overview of current prediction data"))

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(40)
        stats_layout.addWidget(self.create_prediction_stat("Total Affected Area"))
        stats_layout.addWidget(self.create_prediction_stat("Rate of Spread"))
        stats_layout.addWidget(self.create_prediction_stat("Vegetation Patches Count"))
        layout.addLayout(stats_layout)

        return widget

    def create_prediction_stat(self, title):
        widget = QWidget()
        widget.setMinimumSize(150, 150)
        layout = QVBoxLayout(widget)
        lbl_heading = self.ui.create_heading(title)
        layout.addWidget(lbl_heading, alignment=Qt.AlignCenter)
        lbl_stat = QLabel("0")
        lbl_stat.setStyleSheet("color: #000000; font-size: 40px; font-weight: bold")
        layout.addWidget(lbl_stat, alignment=Qt.AlignCenter)
        layout.addSpacing(5)
        return widget

    def create_compare_predictions(self):
        return self.ui.create_card_widget("Compare Predictions",
                                       "Determine the progress of the plant's movement",
                                       "Compare", "Assets/Images/Scanned Image.png")

    def create_recent_predictions(self):
        return self.ui.create_card_widget("Recent Predictions",
                                       "Look back at previous forecasting",
                                       "View", "Assets/Images/Scanned Image.png")

    def create_reports(self):
        return self.ui.create_card_widget("Reports",
                                       "Customise, edit and export valuable insights from reports",
                                       "Generate", "Assets/Images/Scanned Image.png")


