# TODO: Add a QMessage to notify users that their report is saved successfully
import sqlite3
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from views.ui import Interface
from controllers.satellite_imagery import Satellite
from controllers.downloader import DownloadThread

class Data(QWidget):
    def __init__(self, stack,db):
        super().__init__()
        self.stack = stack
        self.ui = Interface(self.stack)
        self.db = db

        # Objects
        sidebar = self.ui.create_sidebar()
        header = self.ui.create_header()

        lbl_title = QLabel("Data Management")

        # Layout
        content_widget = QWidget()
        actions_widget = QWidget()

        content_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QHBoxLayout(content_widget)
        actions_layout = QVBoxLayout(actions_widget)

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
        actions_layout.addWidget(self.create_delete_section())
        actions_layout.addStretch()
        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")

        actions_layout.setSpacing(50)

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

    def create_delete_section(self):
        """Create a section with delete functionality."""
        delete_section = QGroupBox("Delete Data")
        delete_section.setStyleSheet(self.ui.styles["section_style"])

        layout = QHBoxLayout(delete_section)

        # Warning label
        warning_label = QLabel("Warning: This action will permanently delete all vegetation data from the database.")
        warning_label.setStyleSheet("color: red; font-weight: bold;")

        # Delete button
        btn_delete = self.ui.create_tertiary_btn("Reset")
        btn_delete.clicked.connect(self.confirm_delete_data)

        layout.addWidget(warning_label)
        layout.addStretch()
        layout.addWidget(btn_delete)

        return delete_section

    def confirm_delete_data(self):
        """Show confirmation dialog before deleting data."""
        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            'Are you sure you want to delete all vegetation data? This action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.delete_all_data()

    def delete_all_data(self):
        try:
            self.db.delete_all_data()

            QMessageBox.information(
                self,
                'Success',
                'All vegetation data has been successfully deleted.',
                QMessageBox.Ok
            )

            QMessageBox.information(self, 'Restart Needed',
                                    'The app needs to restart to complete resetting the database.'
                                    ' Please close and open the app again.',
                                    QMessageBox.Ok)

        except sqlite3.Error as e:
            QMessageBox.critical(
                self,
                'Error',
                f'{str(e)}',
                QMessageBox.Ok
            )

        finally:
            self.db.close()


    def download_images(self):
        # Open the dialog to ask for directory
        folder = QFileDialog.getExistingDirectory(None, "Select Directory")
        print(f"{folder} folder selected...")


        # Check if a directory was selected
        if folder:
            # Provide start and end date for download (can also ask user for these inputs)
            start_date = self.date_from.date().toString("yyyy-MM-dd")  # Example date input
            end_date = self.date_to.date().toString("yyyy-MM-dd")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")

            # Trigger the download images function
            satellite = Satellite()
            self.download_thread = DownloadThread(satellite, start_date, end_date, folder)

            self.download_thread.start()
        else:
            # Show a message if no directory is selected
            QMessageBox.warning(None, "No Directory Selected", "Please select a directory to save the images.")

    def cancel_download(self):

        if self.download_thread and self.download_thread.isRunning():
            QMessageBox.warning(None, "Cancel Download?", "Are you sure you want to cancel the download?")
            self.add_progress_statement("Cancelling download...")
            self.download_thread.cancel()

