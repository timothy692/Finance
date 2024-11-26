from .dialog import FramelessDialog
from PyQt6.QtCore import Qt as qt
from PyQt6.QtWidgets import *

class TransactionDialog(FramelessDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent, 'Add Transaction', 650, 800)

        tb = self.create_textbox('Description')
        tb.setFixedSize(280, 50)
        self.container.addWidget(tb, alignment=qt.AlignmentFlag.AlignTop)
        

        # Transaction, Amount, Tags, Account?