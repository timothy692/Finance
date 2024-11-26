from .dialog import FramelessDialog
from PyQt6.QtCore import Qt as qt
from PyQt6.QtWidgets import *

class TransactionDialog(FramelessDialog):
    def __init__(self):
        super().__init__('Add Transaction', 650, 800)

        label = QLabel('HELLO')
        label.setStyleSheet('background-color: black;')
        label.setFixedSize(100,100)
        # label.setAlignment(qt.AlignmentFlag.AlignTop)
        self.container.addWidget(label, alignment=qt.AlignmentFlag.AlignTop)