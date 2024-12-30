from PyQt6.QtWidgets import QDateEdit, QCalendarWidget

from widgets.util.styleUtil import load_stylesheet


class Calendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet(
            load_stylesheet('styles/components/calendar.qss')
        )

        self.setGridVisible(False)