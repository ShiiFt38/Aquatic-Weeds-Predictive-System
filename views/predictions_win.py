from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from views.ui import Interface

class Prediction(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        ui = Interface(self.stack)

        # Objects
        sidebar = ui.create_sidebar()
        header = ui.create_header()

        lbl_title = ui.create_title("Prediction Tools")

        lbl_summary = ui.create_heading("Summary")

        # Layout
        content_widget = QWidget()

        content_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QVBoxLayout(content_widget)
        column_area = QHBoxLayout()
        first_column = QVBoxLayout()
        second_column = QVBoxLayout()

        # Inner Layout
        inner_layout.addWidget(sidebar)
        inner_layout.addWidget(content_area, 1)

        # Content layout
        content_layout.addWidget(lbl_title)
        content_layout.addLayout(column_area)
        content_widget.setLayout(content_layout)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)

        # Content Layout > column area
        column_area.addLayout(first_column)
        column_area.addLayout(second_column)
        column_area.setStretch(0, 3)
        column_area.setStretch(1, 1)
        second_column.addWidget(lbl_summary, alignment=Qt.AlignCenter)
        second_column.addStretch()

        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")
