from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
import time
from views.ui import Interface
from controllers.satellite_imagery import Satellite
from controllers.downloader import DownloadThread

class Data(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.ui = Interface(self.stack)

        # Objects
        sidebar = self.ui.create_sidebar()
        header = self.ui.create_header()

        lbl_title = QLabel("Data Management")

        btn_cancel = self.ui.create_tertiary_btn("Cancel")

        progress_box = QGroupBox("Progress Log")

        # Layout
        content_widget = QWidget()
        actions_widget = QWidget()

        content_area = QScrollArea()
        global progress_scroll_area
        progress_scroll_area = QScrollArea()
        progress_scroll_area.setWidget(progress_box)
        progress_scroll_area.setWidgetResizable(True)
        progress_scroll_area.setFixedWidth(300)

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QHBoxLayout(content_widget)
        actions_layout = QVBoxLayout(actions_widget)
        global progress_layout
        progress_layout = QVBoxLayout(progress_box)
        cancel_layout = QVBoxLayout()

        # Inner Layout
        inner_layout.addWidget(sidebar)
        inner_layout.addWidget(content_area, 1)

        # Content layout
        content_layout.addWidget(lbl_title)
        content_widget.setLayout(content_layout)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)
        content_layout.addWidget(actions_widget)

        # actions layout
        actions_layout.addWidget(lbl_title)
        actions_layout.addWidget(self.create_data_section("Satellite Imagery"))
        actions_layout.addWidget(progress_scroll_area)

        # progress layout
        progress_layout.addStretch()
        progress_layout.addLayout(cancel_layout)

        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")

        progress_box.setStyleSheet(self.ui.styles["section_style"])
        progress_box.setMaximumHeight(400)

        # Functions
        btn_cancel.clicked.connect(self.cancel_download)

    def create_data_section(self, title):
        section = QGroupBox(title)
        layout = QHBoxLayout(section)
        section.setStyleSheet(self.ui.styles["section_style"])
        layout.addSpacing(20)

        lbl_choose = self.ui.create_heading("Choose date range")
        layout.addWidget(lbl_choose)
        layout.addStretch()

        lbl_from = self.ui.create_heading("Date From:")
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate())
        calendar = self.date_from.calendarWidget()
        calendar.setStyleSheet(self.ui.calendar_styles)
        layout.addWidget(lbl_from)
        layout.addWidget(self.date_from)
        layout.addSpacing(10)

        lbl_to = self.ui.create_heading("To:")
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        calendar = self.date_to.calendarWidget()
        calendar.setStyleSheet(self.ui.calendar_styles)
        layout.addWidget(lbl_to)
        layout.addWidget(self.date_to)
        layout.addStretch()

        btn_download = self.ui.create_tertiary_btn("Download Images")
        btn_download.clicked.connect(self.download_images)
        layout.addWidget(btn_download)

        return section

    def download_images(self):
        # Open the dialog to ask for directory
        folder = QFileDialog.getExistingDirectory(None, "Select Directory")
        self.add_progress_statement(f"{folder} folder selected...")
        print(f"{folder} folder selected...")

        # Check if a directory was selected
        if folder:
            # Provide start and end date for download (can also ask user for these inputs)
            start_date = self.date_from.date().toString("yyyy-MM-dd")  # Example date input
            end_date = self.date_to.date().toString("yyyy-MM-dd")
            self.add_progress_statement(f"Start Date: {start_date}")
            print(f"Start Date: {start_date}")
            self.add_progress_statement(f"End Date: {end_date}")
            print(f"End Date: {end_date}")

            # Trigger the download images function
            satellite = Satellite()
            self.download_thread = DownloadThread(satellite, start_date, end_date, folder)
            self.add_progress_statement("Starting Download...")

            self.download_thread.start()
            self.add_progress_statement("Connecting to satellite...")
            time.sleep(2)
            self.add_progress_statement("Collection starting...")
            time.sleep(2)
            self.add_progress_statement("Images Collected!")
            time.sleep(2)
            self.add_progress_statement("Image Downloading...")

        else:
            # Show a message if no directory is selected
            QMessageBox.warning(None, "No Directory Selected", "Please select a directory to save the images.")

    def add_progress_statement(self, message):
        """Dynamically add progress statements to the scrollable area."""
        label = QLabel(message)
        progress_layout.addWidget(label)
        progress_layout.addStretch()  # Ensure labels are pushed to the top
        progress_scroll_area.verticalScrollBar().setValue(
        progress_scroll_area.verticalScrollBar().maximum())  # Auto-scroll to bottom

    def cancel_download(self):

        if self.download_thread and self.download_thread.isRunning():
            QMessageBox.warning(None, "Cancel Download?", "Are you sure you want to cancel the download?")
            self.add_progress_statement("Cancelling download...")
            self.download_thread.cancel()

