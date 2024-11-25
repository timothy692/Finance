from PyQt6.QtWidgets import *
from util.style_util import load_stylesheet
from PyQt6.QtCore import Qt as qt

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

        # Separator layout

        separator_layout = QVBoxLayout()
        separator_layout.setContentsMargins(0,0,0,0)

        separator = QFrame()
        separator.setFixedHeight(2)
        separator.setStyleSheet(
            'background-color: #c8c8c8;'
        )
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator_layout.addWidget(separator)

        # Bottom layout

        self.layout_bottom = QVBoxLayout()
        self.layout_bottom.setContentsMargins(25,25,25,25)
        self.layout_bottom.setSpacing(30)

        layout.addLayout(self.layout_top)
        layout.addLayout(separator_layout)
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