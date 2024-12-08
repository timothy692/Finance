from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QMargins
from widgets.util.style_util import load_stylesheet

class Separator(QFrame):
    def __init__(self, color=QColor(166, 166, 166, 250), height=1):
        super().__init__()

        self.setFixedHeight(height)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet(
            f'background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()});'
        )

        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)