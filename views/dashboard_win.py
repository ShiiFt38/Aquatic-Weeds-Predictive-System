import sqlite3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from views.ui import Interface

class Dashboard(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.db = db
        self.ui = Interface(self.stack)

        # Objects
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Date",
            "Image Path",
            "Vegetation Count",
            "Total Area",
            "Avg Area",
            "Details"
        ])

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        # Track labels for statistics
        self.lbl_stats = {
            "Date": None,
            "Total Area Covered": None,
            "Vegetation Patches Count": None
        }

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
        widget.setStyleSheet("""
            QWidget {
                background-color: #E2E2E2; 
                border-radius: 10px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                gridline-color: #f0f0f0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)
        widget.setMaximumSize(1100, 400)
        layout = QVBoxLayout(widget)
        lbl_heading = self.ui.create_heading("Prediction History")
        layout.addWidget(lbl_heading)

        layout.addWidget(self.table)

        return widget

    def refresh_prediction_history(self):
        print("Populating prediction table...")
        try:
            # Get data from the database
            data = self.db.get_history_prediction()

            # Update the statistics with the new data
            self.update_stats()

            # Set the row count to match the number of records
            self.table.setRowCount(len(data))

            # Loop through each record to populate the table
            for row, record in enumerate(data):
                if record[3] != 0:
                    self.table.setItem(row, 0, QTableWidgetItem(record[1] or "N/A"))  # Date
                    self.table.setItem(row, 1, QTableWidgetItem(record[2] or "N/A"))  # Image Path
                    self.table.setItem(row, 2, QTableWidgetItem(str(record[3])))  # Vegetation Count
                    self.table.setItem(row, 3, QTableWidgetItem(f"{record[4]:.2f}"))  # Total Area
                    self.table.setItem(row, 4, QTableWidgetItem(f"{record[5]:.2f}"))  # Avg Area
                    # Below includes columns, max_temp, min_temp, precipitation, rainfall, and max_wind
                    details = (f"Max temperature: {record[6]}\N{DEGREE SIGN}C, Min temperature: {record[7]}\N{DEGREE SIGN}C, "
                               f"Total Precipitation: {record[8]}mm, Rainfall: {record[9]}mm,"
                               f" Maximum wind speed: {record[10]}km/h")
                    self.table.setItem(row, 5, QTableWidgetItem(details))
                else:
                    pass
        except sqlite3.Error as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Error occurred while accessing database: {str(e)}',
                QMessageBox.Ok
            )

    def create_new_prediction(self):
        return self.ui.create_card_widget("New Prediction",
                                       "Enhance image quality with advanced AI. ",
                                       "New", "Assets/Images/undraw_Predictive_analytics_re_wxt8.png", lambda: self.stack.setCurrentIndex(2))

    def create_current_prediction(self):
        widget = QGroupBox("Current Prediction")
        widget.setStyleSheet("""
            QGroupBox {
                padding: 20px 20px 20px 10px;
                border: 1px solid black;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 10px;
                }
        """)
        widget.setMaximumSize(1500, 400)
        layout = QVBoxLayout(widget)
        lbl_description = (QLabel("Overview of current prediction data"))
        layout.addWidget(lbl_description, alignment = Qt.AlignCenter )

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(40)
        stats_layout.addWidget(self.create_prediction_stat("Date"))
        stats_layout.addWidget(self.create_prediction_stat("Total Area Covered"))
        stats_layout.addWidget(self.create_prediction_stat("Vegetation Patches Count"))
        layout.addLayout(stats_layout)

        return widget

    def create_prediction_stat(self, title):
        widget = QWidget()
        widget.setMinimumSize(300, 150)
        layout = QVBoxLayout(widget)
        lbl_heading = self.ui.create_heading(title)
        layout.addWidget(lbl_heading, alignment=Qt.AlignCenter)
        lbl_stat = QLabel("0")
        lbl_stat.setStyleSheet("color: #000000; font-size: 40px; font-weight: bold")
        layout.addWidget(lbl_stat, alignment=Qt.AlignCenter)
        layout.addSpacing(5)

        # Save the lbl_stat for future updates
        self.lbl_stats[title] = lbl_stat

        return widget

    def update_stats(self):
        print("Updating statistics...")

        # Get the last row index in the table
        first_row = 0
        if first_row < 0:
            return  # No rows available, exit the function

        try:
            # Retrieve data from the last row in the table
            date = self.table.item(first_row, 0).text() if self.table.item(first_row, 0) else "N/A"
            vegetation_count = int(self.table.item(first_row, 2).text()) if self.table.item(first_row, 2) else "N/A"
            total_area = float(self.table.item(first_row, 3).text()) if self.table.item(first_row, 3) else "N/A"

            # Update your statistics variables or UI elements with this data
            self.lbl_stats["Date"].setText(f"{date}")
            self.lbl_stats["Total Area Covered"].setText(f"{total_area}")
            self.lbl_stats["Vegetation Patches Count"].setText(str(vegetation_count))

        except Exception as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Error occurred while updating statistics: {str(e)}',
                QMessageBox.Ok
            )

    def create_compare_predictions(self):
        return self.ui.create_card_widget("Compare Predictions",
                                       "Determine the progress of the plant's movement",
                                       "Compare", "Assets/Images/undraw_split_testing_l1uw.png")

    def create_recent_predictions(self):
        btn_refresh = self.ui.create_card_widget("Update Predictions",
                                   "Look back at previous forecasting",
                                   "Refresh", "Assets/Images/undraw_Booking_re_gw4j.png", self.refresh_prediction_history)

        return btn_refresh

    def create_reports(self):
        return self.ui.create_card_widget("Reports",
                                       "Customise, edit and export valuable insights from reports",
                                       "Generate", "Assets/Images/undraw_Done_checking_re_6vyx.png", lambda: self.stack.setCurrentIndex(3))


