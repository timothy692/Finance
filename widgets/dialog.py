from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt as qt, QSize, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QColor
from util.style_util import load_stylesheet

class FramelessDialog(QDialog):
    def __init__(self, parent: QWidget, title: str, width: int, height: int):
        super().__init__(parent)

        self.setWindowFlags(
            qt.WindowType.FramelessWindowHint | qt.WindowType.Window
        )

        # self.setAttribute(qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.title = title
        self.setModal(True)
        self.setFixedSize(width, height)

        self.setStyleSheet(
            load_stylesheet('styles/dialog.qss')
        )

        self._init_gui()

        self._is_dragging = False
        self._drag_position = QPoint()

    def create_textbox(self, placeholder: str) -> QLineEdit:
        tb = QLineEdit()
        tb.setObjectName('textbox')
        tb.setPlaceholderText(placeholder)
        tb.setReadOnly(False)
        return tb
    
    def create_widget_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName('widget-label')
        label.setFixedHeight(25)
        return label

    def _init_gui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # Separator

        separator_layout = QVBoxLayout()
        separator_layout.setContentsMargins(0,0,0,0)

        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(
            'background-color: rgba(166, 166, 166, 250)'
        )
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator_layout.addWidget(separator)

        # Top bar

        self.top_bar = QHBoxLayout()
        self.top_bar.setContentsMargins(25,20,25,10)
        
        title = QLabel(self.title)
        title.setObjectName('title')
        
        close = QPushButton()
        close.setIcon(QIcon(
            QPixmap('assets/icons/close.png').scaled(21, 21, 
                                              qt.AspectRatioMode.KeepAspectRatio,
                                              qt.TransformationMode.SmoothTransformation)
        ))
        close.setIconSize(QSize(21,21))

        close.setStyleSheet(
            '''
            background-color: transparent; 
            border: none;
            '''
        )

        close.clicked.connect(self.close)

        self.top_bar.addStretch()
        self.top_bar.addWidget(title, alignment=qt.AlignmentFlag.AlignCenter)
        self.top_bar.addStretch()
        self.top_bar.addWidget(close, alignment=qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(self.top_bar)
        layout.addLayout(separator_layout)
        layout.addStretch()

        self.container = QVBoxLayout()
        self.container.setContentsMargins(30,20,30,30)
        self.container.setSpacing(0)

        layout.addLayout(self.container, stretch=1)

        self.setLayout(layout)

    def center(self):
        if self.parent():
            parent_geometry = self.parent().geometry()
            dialog_geometry = self.frameGeometry()
            dialog_geometry.moveCenter(parent_geometry.center())
            self.move(dialog_geometry.topLeft())

    def keyPressEvent(self, event):
        if event.key() == qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)