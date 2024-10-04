from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from views.ui import Interface

class Report(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

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
        section.setStyleSheet("""
            QGroupBox {
                padding: 50px 50px 50px 50px;
                border: 1px solid black;
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                }
        """)
        layout.addSpacing(20)

        lbl_choose = self.ui.create_heading("Choose date range")
        layout.addWidget(lbl_choose)
        layout.addStretch()

        lbl_from = self.ui.create_heading("Date From:")
        date_from = QDateEdit()
        date_from.setCalendarPopup(True)
        date_from.setDate(QDate.currentDate())
        layout.addWidget(lbl_from)
        layout.addWidget(date_from)
        layout.addSpacing(10)

        lbl_to = self.ui.create_heading("To:")
        date_to = QDateEdit()
        date_to.setCalendarPopup(True)
        date_to.setDate(QDate.currentDate())
        layout.addWidget(lbl_to)
        layout.addWidget(date_to)
        layout.addStretch()

        btn_generate = self.ui.create_tertiary_btn("Generate Report")
        layout.addWidget(btn_generate)

        return section

