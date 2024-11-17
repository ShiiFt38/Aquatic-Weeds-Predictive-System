from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from views.ui import Interface
from PyQt5.QtCore import Qt

class About(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        ui = Interface(self.stack)

        lbl_awps = ui.create_title("Aquatic Weeds Predictive System")
        lbl_version = QLabel("Version 0.8.2")
        btn_close = ui.create_primary_btn("Close")

        #Layout
        main_layout = QVBoxLayout()

        main_layout.addWidget(lbl_awps, alignment=Qt.AlignCenter)
        main_layout.addWidget(lbl_version, alignment=Qt.AlignCenter)
        main_layout.addSpacing(-50)
        main_layout.addWidget(btn_close, alignment=Qt.AlignCenter)

        # Functions
        btn_close.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        self.setLayout(main_layout)
