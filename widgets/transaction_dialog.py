from .dialog import FramelessDialog

class TransactionDialog(FramelessDialog):
    def __init__(self):
        super().__init__('Add Transaction', 500, 700)

    