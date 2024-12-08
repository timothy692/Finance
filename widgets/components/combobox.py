from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate, QApplication, QStyle
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt as qt, QEvent, QSize
from widgets.util.drop_shadow import DropShadowEffect
from widgets.util.style_util import load_stylesheet

class ComboBoxItemDelegate(QStyledItemDelegate):
    def __init__(self, height: int):
        super().__init__()
        self.item_height = height

    def sizeHint(self, option, index):
        # Set custom height for each item
        size = super().sizeHint(option, index)
        return QSize(size.width(), self.item_height)
    
class ComboBox(QComboBox):
    def __init__(self, text: str, width: int, height: int, effect: DropShadowEffect=None):
        super().__init__()

        self.setStyleSheet(
            load_stylesheet('styles/components/combobox.qss')
        )        

        self._text = text
        self.setFixedSize(width, height)

        self.setEditable(True)

        self.clearEditText()
        self.lineEdit().setText(self._text)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setCursorPosition(0)

        self.lineEdit().setFocusPolicy(qt.FocusPolicy.NoFocus)

        self.view().setVerticalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view().setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setItemDelegate(ComboBoxItemDelegate(40))

        if effect:
            effect.register_events([QEvent.Type.FocusIn])
            effect.apply(parent=self)

        self.currentIndexChanged.connect(self._reset_text)

    def _reset_text(self):
        """Keep the line edit text static."""
        self.lineEdit().setText(self._text)