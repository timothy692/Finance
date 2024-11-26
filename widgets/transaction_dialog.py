from .dialog import FramelessDialog
from PyQt6.QtCore import Qt as qt
from PyQt6.QtWidgets import *

class TransactionDialog(FramelessDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent, 'Add Transaction', 650, 800)

        description_layout = QVBoxLayout()
        description_layout.setSpacing(10)
        description_layout.addWidget(
            self.create_widget_label('Description')
        )

        textbox = self.create_textbox('Description')
        textbox.setFixedSize(280, 50)
        
        description_layout.addWidget(textbox)

        self.container.addLayout(description_layout)
        # self.container.addWidget(tb, alignment=qt.AlignmentFlag.AlignTop)
        

        # Transaction, Amount, Tags, Account?