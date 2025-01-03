from __future__ import annotations

from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QLabel,
                             QLayout, QLineEdit, QVBoxLayout)

from widgets.util.dropshadow import DropShadowEffect
from widgets.util.styleUtil import load_stylesheet


class Input(QVBoxLayout):
    def __init__(self, placeholder: str, width: int, height=40, border_radius=10, effect: DropShadowEffect=None) -> None:
        super().__init__()

        self.layout().setContentsMargins(0,0,0,0)

        tb = QLineEdit()
        tb.setReadOnly(False)
        tb.setPlaceholderText(placeholder)
        tb.setFixedSize(width, height)

        tb.setStyleSheet(
            load_stylesheet('styles/components/input.qss') +
            f'''
            QLineEdit {{
                border-radius: {border_radius};
            }}
            '''
        )

        if effect:
            effect.register_events([QEvent.Type.HoverEnter, QEvent.Type.FocusIn])
            effect.apply(parent=tb)

        self._textbox = tb
        self._label = None

    def add_input_label(self, text: str, padding=7) -> Input:
        label = QLabel(text)
        label.setStyleSheet(
            load_stylesheet('styles/components/input.qss')
        )

        self._label = label
        self.layout().setSpacing(padding)

        return self

    def get_textbox(self) -> QLineEdit:
        return self._textbox
    
    def get_label(self) -> QLabel:
        return self._label

    def build(self) -> QVBoxLayout:
        if self._label:
            self.layout().addWidget(self._label)

        self.layout().addWidget(self._textbox)

        return self.layout()