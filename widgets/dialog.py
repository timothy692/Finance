from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt as qt, QSize, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QColor
from util.style_util import load_stylesheet

class FramelessDialog(QDialog):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()

        self.setWindowFlags(
            qt.WindowType.FramelessWindowHint | qt.WindowType.Window
        )

        self.setAttribute(qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.title = title
        self.setModal(True)
        self.setFixedSize(width, height)

        self.setStyleSheet(
            load_stylesheet('styles/dialog.qss')
        )

        self._init_gui()

        self._is_dragging = False
        self._drag_position = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen_width = 2
        pen = QPen(QColor('#E0E0E0'), pen_width)
        painter.setPen(pen)

        painter.setBrush(QBrush(QColor('white')))

        # Adjust rect to avoid overlap
        rect = self.rect().adjusted(pen_width // 2, pen_width // 2, -pen_width // 2, -pen_width // 2)
        painter.drawRoundedRect(rect, 15, 15)

    def _init_gui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # Separator

        separator_layout = QVBoxLayout()
        separator_layout.setContentsMargins(0,0,0,0)

        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet(
            'background-color: #F0F0F0;'
        )
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator_layout.addWidget(separator)

        # Top bar

        self.top_bar = QHBoxLayout()
        self.top_bar.setContentsMargins(30,20,30,10)
        
        title = QLabel(self.title)
        title.setObjectName('title')
        
        close = QPushButton()
        close.setIcon(QIcon(
            QPixmap('assets/close.png').scaled(20, 20, 
                                              qt.AspectRatioMode.KeepAspectRatio,
                                              qt.TransformationMode.SmoothTransformation)
        ))
        close.setIconSize(QSize(20,20))

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

        self.setLayout(layout)

    def _is_in_top_bar(self, pos):
        """Check if the click is within the top bar."""
        bar_height = self.top_bar.geometry().height()
        return 0 <= pos.y() <= bar_height

    def mousePressEvent(self, event):
        if event.button() == qt.MouseButton.LeftButton and self._is_in_top_bar(event.pos()):
            self._is_dragging = True
            self._drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging and event.buttons() == qt.MouseButton.LeftButton:
            # Calculate the delta and move the dialog
            delta = event.globalPosition().toPoint() - self._drag_position
            self.move(self.pos() + delta)
            self._drag_position = event.globalPosition().toPoint()  # Update the last drag position
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == qt.MouseButton.LeftButton:
            self._is_dragging = False
            event.accept()

    def keyPressEvent(self, event):
        if event.key() == qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)