from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *

from models.tag import TagManager
from widgets.util.styleUtil import load_stylesheet
from widgets.components.separator import Separator


class Page(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('page')

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Top layout

        self.layout_top = QHBoxLayout()
        self.layout_top.setContentsMargins(15,15,15,15)
        self.layout_top.setSpacing(0)
        frame = QFrame()
        frame.setFixedHeight(30)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_top.addWidget(frame)

        # Bottom layout

        self.layout_bottom = QVBoxLayout()
        self.layout_bottom.setContentsMargins(20,20,20,20)
        self.layout_bottom.setSpacing(30)

        layout.addLayout(self.layout_top)
        layout.addWidget(Separator())
        layout.addLayout(self.layout_bottom, stretch=2)

        self._init_top_container()
        self._init_bottom_container()

        self.setStyleSheet(
            load_stylesheet('styles/page.qss')
        )

    def _init_top_container(self) -> None:
        pass

    def _init_bottom_container(self) -> None:
        pass