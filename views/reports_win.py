# TODO: Add generating documents functionality
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from views.ui import Interface
from controllers.file_exporter import ExportReports
from models.db_export_utility import ExportUtility

class Report(QWidget):
    def __init__(self, stack, db):
        super().__init__()
        self.stack = stack
        self.db = db
        self.ui = Interface(self.stack)

        # Objects
        sidebar = self.ui.create_sidebar()
        header = self.ui.create_header()

        lbl_title = self.ui.create_title("Reports")

        # Layout
        content_widget = QWidget()
        reports_widget = QWidget()

        content_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QVBoxLayout(content_widget)
        reports_layout = QVBoxLayout(reports_widget)

        # Inner Layout
        inner_layout.addWidget(sidebar)
        inner_layout.addWidget(content_area, 1)

        # Content layout
        content_layout.addWidget(lbl_title)
        content_widget.setLayout(content_layout)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)
        content_layout.addWidget(reports_widget)

        # Reports layout
        reports_layout.addWidget(lbl_title)
        reports_layout.addWidget(self.create_report_section("Generate PDF Report"))
        reports_layout.addWidget(self.create_report_section("Generate Excel Report"))
        reports_layout.addWidget(self.create_report_section("Generate CSV Report"))
        reports_layout.addStretch()
        reports_layout.setSpacing(50)

        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")

        # Functions
    def create_report_section(self, title):
        section = QGroupBox(title)
        layout = QHBoxLayout(section)
        section.setStyleSheet(self.ui.styles["section_style"])
        layout.addSpacing(20)

        lbl_choose = self.ui.create_heading("Choose date range")
        layout.addWidget(lbl_choose)
        layout.addStretch()

        lbl_from = self.ui.create_heading("Date From:")
        date_from = QDateEdit()
        date_from.setCalendarPopup(True)
        date_from.setDate(QDate.currentDate())
        calendar = date_from.calendarWidget()
        calendar.setStyleSheet(self.ui.calendar_styles)
        layout.addWidget(lbl_from)
        layout.addWidget(date_from)
        layout.addSpacing(10)

        lbl_to = self.ui.create_heading("To:")
        date_to = QDateEdit()
        date_to.setCalendarPopup(True)
        date_to.setDate(QDate.currentDate())
        calendar = date_to.calendarWidget()
        calendar.setStyleSheet(self.ui.calendar_styles)
        layout.addWidget(lbl_to)
        layout.addWidget(date_to)
        layout.addStretch()

        btn_generate = self.ui.create_tertiary_btn("Generate Report")
        btn_generate.clicked.connect(lambda: self.generate_report(title, date_from, date_to))
        layout.addWidget(btn_generate)

        return section

    def generate_report(self, report_type, date_from, date_to):
        exporter = ExportReports(self.db)
        export_utility = ExportUtility(self.db)

        start_date = date_from.date().toString("yyyy-MM-dd")
        end_date = date_to.date().toString("yyyy-MM-dd")

        data = export_utility.export_vegetation_data(start_date, end_date)

        file_path = QFileDialog.getSaveFileName(self, "Save Excel Report",
                                                "", "Excel Files (*.xlsx)")[0]
        if not file_path:
            return

        print("Saving excel file")
        if "Excel" in report_type:
            if not file_path.endswith(".xlsx"):
                file_path += ".xlsx"
            print(f"Saving to {file_path}")
            exporter.save_to_excel(data, file_path)
        else:
            pass

