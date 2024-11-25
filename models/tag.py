from dataclasses import dataclass
from PyQt6.QtGui import QColor

@dataclass
class Tag:
    text: str
    background_color: QColor
    text_color: QColor