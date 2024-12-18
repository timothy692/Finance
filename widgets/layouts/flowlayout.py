from PyQt6.QtWidgets import QLayout, QSizePolicy, QWidgetItem
from PyQt6.QtCore import QSize, QRect, QPoint

class FlowLayout(QLayout):
    def __init__(self, parent=None, spacing=10):
        super().__init__(parent)
        self._items = []  # List to hold layout items
        self.setSpacing(spacing)  # Horizontal/Vertical spacing

    def addItem(self, item):
        """Add an item to the layout."""
        self._items.append(item)

    def sizeHint(self):
        """Provide a size hint for the layout."""
        return QSize(200, 200)

    def count(self):
        """Return the number of items in the layout."""
        return len(self._items)

    def itemAt(self, index):
        """Return the item at a specific index."""
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        """Remove and return the item at a specific index."""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def setGeometry(self, rect):
        """Position and size all items within the given rectangle."""
        super().setGeometry(rect)
        x, y = rect.x(), rect.y()
        row_height = 0

        for item in self._items:
            widget = item.widget()
            widget_size = widget.sizeHint()

            # Check if the widget fits in the current row
            if x + widget_size.width() > rect.right() and x > rect.x():
                x = rect.x()  # Move to the start of the next row
                y += row_height + self.spacing()
                row_height = 0

            # Set widget geometry
            item.setGeometry(QRect(QPoint(x, y), widget_size))

            # Update x and row height
            x += widget_size.width() + self.spacing()
            row_height = max(row_height, widget_size.height())

    def hasHeightForWidth(self):
        """Indicate that the layout supports height-for-width."""
        return True

    def heightForWidth(self, width):
        """Calculate the height of the layout given a width."""
        x = 0
        y = 0
        row_height = 0

        for item in self._items:
            widget_size = item.widget().sizeHint()

            if x + widget_size.width() > width:
                x = 0
                y += row_height + self.spacing()
                row_height = 0

            x += widget_size.width() + self.spacing()
            row_height = max(row_height, widget_size.height())

        return y + row_height
