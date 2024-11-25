from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox, QComboBox, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt as qt
from util.style_util import load_stylesheet

class FramelessDialog(QDialog):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()

        self.setWindowFlags(qt.WindowType.FramelessWindowHint)
        # self.setAttribute(qt.WidgetAttribute.WA_TranslucentBackground)

        self.title = title
        self.setModal(True)
        self.setFixedSize(width, height)

        self.setStyleSheet(
            load_stylesheet('styles/dialog.qss')
        )

        self._init_gui()

    def _init_gui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(10,10,10,10)
        
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        title = QLabel(self.title)
        title.setObjectName('title')
        top_bar.addWidget(title, alignment=qt.AlignmentFlag.AlignHCenter)


        layout.addStretch()
        layout.addLayout(top_bar)
        self.setLayout(layout)