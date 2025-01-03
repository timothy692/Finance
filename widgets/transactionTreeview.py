from typing import List

from PyQt6.QtGui import QPen, QFont, QColor, QPainter
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QRectF, QModelIndex, QAbstractTableModel
from PyQt6.QtWidgets import *

from models.tag import Tag


class PaddingDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        option.rect.adjust(60, 0, 0, 0)
        super().paint(painter, option, index)

class TagDelegate(QStyledItemDelegate):
    def __init__(self, tags: List[Tag]):
        super().__init__()
        self.tags = tags

    def paint(self, painter, option, index) -> None:
        # Get the tags from the model
        tags = index.data(qt.ItemDataRole.DisplayRole)
        if not tags:
            return

        if not isinstance(tags, list):
            tags = [tags]

        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        font = QFont("Inter Medium", 10)
        painter.setFont(font)

        padding = 6 # Increase padding for more spacing around the text
        spacing = 6 # Space between tags
        alignment_offset = 60 # Additional alignment padding to shift tags right

        font_metrics = painter.fontMetrics()
        text_height = font_metrics.height()
        tag_height = text_height + 6 # Height of tag

        # Start at the left edge of the "Tag" column
        x_offset = option.rect.x() + alignment_offset
        y_offset = option.rect.y() + (option.rect.height() - tag_height) // 2  # Center vertically

        for tag in tags:
            painter.setBrush(tag.background)
            painter.setPen(QPen(QColor(211, 211, 211, 100), 1))

            # Measure the size of the tag
            tag_width = font_metrics.horizontalAdvance(tag.text) + padding * 2
            tag_rect = QRectF(x_offset, y_offset, tag_width, tag_height)

            # Draw the rounded rectangle (background)
            painter.drawRoundedRect(tag_rect, 6, 6) 

            # Draw the text
            painter.setPen(tag.foreground)
            painter.drawText(tag_rect, qt.AlignmentFlag.AlignCenter, tag.text)

            # Update x_offset for the next tag
            x_offset += tag_width + spacing # Spacing between tags

        painter.restore()

class TransactionTableModel(QAbstractTableModel):
    def __init__(self, data: List[List]):
        super().__init__()

        self.data_list = data
        self.headers = ['Date', 'Transaction', 'Amount', 'Tag', 'Account']

    def rowCount(self, parent=None) -> int:
        return len(self.data_list)
    
    def columnCount(self, parent=None) -> int:
        return len(self.headers)
    
    def get_data_list(self) -> List[List]:
        return self.data_list
    
    def add_data(self, data: List) -> None:
        self.data_list.append(data)

    def remove_data(self, index: int) -> bool:
        if index > len(self.data_list):
            return False
        
        self.data_list.pop(index)
        return True

    def data(self, index: int, role: qt.ItemDataRole.DisplayRole) -> None:
        if not index.isValid():
            return None

        row, col = index.row(), index.column()
        value = self.data_list[row][col]
        
        if role == qt.ItemDataRole.DisplayRole:
            # Special formatting for amount column
            if col == 2:
                return f'{'+ ' if value > 0 else ''}${abs(value):,.2f}'
            
            return value
        
        # Green foreground for positive values in amount column
        if role == qt.ItemDataRole.ForegroundRole and col == 2:
            return QColor('black') if value < 0 else QColor('green')
        
        return None
    
    def headerData(self, section: int, orientation: qt.Orientation, role: qt.ItemDataRole) -> None:
        if role == qt.ItemDataRole.DisplayRole and orientation == qt.Orientation.Horizontal:
            return self.headers[section]
        return None
    
class TransactionTreeview(QTreeView):
    def __init__(self, tags: List[Tag]):
        super().__init__()
        self.tags = tags

        self._model = TransactionTableModel([])
        self.setModel(self._model)

        header = self.header()
        header.setSectionsMovable(False)
        header.setStretchLastSection(True)
        header.setFixedHeight(40)

        header.resizeSection(0, 160) # Date - Transaction
        header.resizeSection(1, 250) # Transaction - Amount
        header.resizeSection(2, 160) # Amount - Tag
        header.resizeSection(3, 200) # Tag - Account
        header.resizeSection(4, 80) # Account 

        self.setRootIsDecorated(False)
        self.setSelectionMode(QTreeView.SelectionMode.NoSelection) 
        self.setFocusPolicy(qt.FocusPolicy.NoFocus)
        self.setUniformRowHeights(False)
        self.setWordWrap(True)
        self.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.setItemDelegate(PaddingDelegate(self))
        self.setItemDelegateForColumn(3, TagDelegate(self.tags))

    def add_entry(self, entry: List[List]):
        """ 
        Add a row to the treeview (date, description, amount, tags, account)
        """

        pos = len(self._model.get_data_list())
        self._model.beginInsertRows(QModelIndex(), pos, pos)
        self._model.add_data(entry)
        self._model.endInsertRows()