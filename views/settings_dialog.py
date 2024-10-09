from PyQt5.QtWidgets import *
from views.ui import Interface

class Settings():
    def __init__(self, stack):
        super().__init__(self)
        self.stack = stack

        ui = Interface(self.stack)

        # Objects
        sidebar = ui.create_sidebar()
        header = ui.create_header()

        lbl_title = QLabel("Settings")

        earth_config_section = QGroupBox("EarthEngine Configuration")

        # Layout
        content_widget = QWidget()

        content_area = QScrollArea()

        main_layout = QVBoxLayout()
        inner_layout = QHBoxLayout()
        content_layout = QVBoxLayout(content_widget)

        # Inner Layout
        inner_layout.addWidget(sidebar)
        inner_layout.addWidget(content_area, 1)

        # Content layout
        content_layout.addWidget(lbl_title)
        content_widget.setLayout(content_layout)
        content_area.setWidget(content_widget)
        content_area.setWidgetResizable(True)

        main_layout.addWidget(header)
        main_layout.addLayout(inner_layout)

        self.setLayout(main_layout)

        # Design
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0;")
        content_area.setStyleSheet("border: none")