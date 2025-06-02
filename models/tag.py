from dataclasses import dataclass

from PyQt6.QtGui import QColor

from .dataModel import DataModel


@dataclass
class Tag(DataModel):
    key: str
    text: str
    background: QColor
    foreground: QColor

    def is_valid(self) -> bool:
        return len(self.text) <= 16
    
    def to_tuple(self):
        return (self.key, self.text, self.background, self.foreground)