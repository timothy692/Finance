from PyQt6.QtCore import QEvent, QModelIndex, QPoint, QPointF, QRectF, QSize
from PyQt6.QtCore import Qt as qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPalette
from PyQt6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox,
                             QStyle, QStyledItemDelegate, QStyleOptionViewItem)

from widgets.util.dropshadow import DropShadowEffect
from widgets.util.styleUtil import load_stylesheet


class ComboBoxItemDelegate(QStyledItemDelegate):
    def __init__(self, height, parent=None):
        super().__init__(parent)
        self.hover_color = QColor("#f8f8fa")  # Light grey for hover effect
        self.text_color = QColor("black")  # Text color
        self.padding = 10 
        self.height = height

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        """
        Custom paint method to define the item's appearance with rounded corners
        """

        painter.save()

        # Determine item state
        is_hovered = option.state & QStyle.StateFlag.State_MouseOver        

        # Rounded borders
        rect = option.rect.adjusted(1, 1, -1, -1).toRectF()
        radius = 5

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        if is_hovered:
            painter.fillPath(path, self.hover_color)
        else:
            painter.fillPath(path, QColor("white")) 

        # Set font and text color
        painter.setFont(QFont('Inter Regular', 11))
        painter.setPen(self.text_color)

        text_rect = option.rect.adjusted(self.padding, 0, -self.padding, 0) # Add horizontal padding
        painter.drawText(text_rect, qt.AlignmentFlag.AlignVCenter | qt.AlignmentFlag.AlignLeft, index.data())

        # Restore painter state
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        """
        Define a consistent size for each item
        """

        size = super().sizeHint(option, index)
        return QSize(size.width(), self.height)
    
class ComboBox(QComboBox):
    def __init__(self, width: int, height: int, border_radius=10, effect: DropShadowEffect=None):
        super().__init__()    
        self.item_height = 32

        self.setFixedSize(width, height)

        self.setEditable(True)

        self.lineEdit().setReadOnly(True)
        self.lineEdit().setCursorPosition(0)
        self.lineEdit().setFocusPolicy(qt.FocusPolicy.NoFocus)

        self.setItemDelegate(ComboBoxItemDelegate(self.item_height))
        self.setFocusPolicy(qt.FocusPolicy.StrongFocus)

        self.view().setVerticalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view().setAutoScroll(False)
        self.view().setFocusPolicy(qt.FocusPolicy.NoFocus)

        self.setStyleSheet(
            load_stylesheet('styles/components/combobox.qss') + 
            f'''
            QComboBox {{
                border-radius: {border_radius};
            }}
            '''
        )    

        self._effect = effect
        if effect:
            effect.register_events([])
            effect.apply(parent=self)

    def showPopup(self):
        # Apply shadow effect when popup is shown
        if self._effect:
            self._effect.enable()

        list_height = self.count() * self.item_height
        self.view().setFixedHeight(list_height + int(self.item_height * .3))

        super().showPopup()

    def hidePopup(self):
        # Remove shadow effect when popup is hidden
        if self._effect:
            self._effect.disable()

        super().hidePopup()