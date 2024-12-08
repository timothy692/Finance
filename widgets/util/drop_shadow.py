from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QWidget
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QObject, QEvent
from typing import List

class DropShadowEffect(QObject):
    def __init__(self, color=QColor(60, 64, 188, 100), blur_radius=20, dy_offset=0):
        super().__init__()

        self._blur_radius = blur_radius
        self._color = color

        self.effect = QGraphicsDropShadowEffect()
        self.effect.setOffset(0, dy_offset)
        self.effect.setColor(self._color)

        self._trigger_events = []

        self._inverse_events = {
            QEvent.Type.FocusIn: QEvent.Type.FocusOut,
            QEvent.Type.HoverEnter: QEvent.Type.HoverLeave
        }

    def apply(self, parent=QWidget, always_enable=False) -> QWidget:
        """
        Apply shadow effect to the given widget
        """

        self.setParent(parent)

        self._parent = parent
        self._always_enable = always_enable

        # Attach effect to parent
        parent.setGraphicsEffect(self.effect)

        self.effect.setBlurRadius(self._blur_radius)

        # Install event filter to handle focus and hover events if not always enabled
        if not always_enable:
            self.effect.setBlurRadius(0)
            parent.installEventFilter(self)

        return self.parent

    def register_events(self, events: List[QEvent.Type]) -> None:
        self._trigger_events.extend(events)

    def eventFilter(self, obj, event):
        if obj == self._parent and len(self._trigger_events) > 0:
            # Enable / disable effect by changing blur radius
            if event.type() in self._trigger_events:
                self.effect.setBlurRadius(self._blur_radius)
            elif event.type() in self._inverse_events.values():
                self.effect.setBlurRadius(0)
            
            
        return super().eventFilter(obj, event)