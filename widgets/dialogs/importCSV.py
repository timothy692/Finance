from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit, QCalendarWidget

from widgets.components.calendar import Calendar

from .dialog import FramelessDialog


class ImportCSV(FramelessDialog):
    def __init__(self, parent):
        super().__init__(parent, 'Import CSV', 350, 450)

    def init(self):
        calendar = Calendar()

        self.container.addWidget(calendar)