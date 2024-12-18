from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor
from widgets.util.style_util import load_stylesheet
from widgets.components.separator import Separator
from models.tag import TagManager

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
        frame.setFixedHeight(70)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_top.addWidget(frame)

        # Bottom layout

        self.layout_bottom = QVBoxLayout()
        self.layout_bottom.setContentsMargins(25,25,25,25)
        self.layout_bottom.setSpacing(30)

        layout.addLayout(self.layout_top)
        layout.addWidget(Separator(color=(QColor(200,200,200)), height=1))
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