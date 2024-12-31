from dataclasses import dataclass

from PyQt6.QtGui import QColor


@dataclass
class Tag:
    key: str
    text: str
    background: QColor
    foreground: QColor

    def is_valid(self) -> bool:
        return len(self.text) <= 16