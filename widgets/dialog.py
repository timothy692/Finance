from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt as qt, QSize, QPoint
from PyQt6.QtGui import QIcon, QPixmap, QColor
from widgets.util.style_util import load_stylesheet
from widgets.util.drop_shadow import DropShadowEffect
from widgets.components.separator import Separator

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

        self._padding = 40

        self._init_gui()

    def total_width(self) -> int:
        return self.width() - self._padding*2
    
    def create_widget_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName('widget-label')
        label.setFixedHeight(25)
        return label

    def _init_gui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # Top bar

        self.top_bar = QHBoxLayout()
        self.top_bar.setContentsMargins(25,20,25,10)
        
        title = QLabel(self.title)
        title.setObjectName('title')
        
        close = QPushButton()
        close.setCursor(qt.CursorShape.PointingHandCursor)
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
        layout.addWidget(Separator())

        self.container = QVBoxLayout()
        self.container.setContentsMargins(self._padding,30,self._padding,self._padding)
        self.container.setSpacing(0)

        layout.addLayout(self.container, stretch=1)

        bottom_bar_container = QWidget(self)
        bottom_bar_container.setObjectName('bottom-bar')

        self.bottom_bar = QHBoxLayout(bottom_bar_container)
        self.bottom_bar.setContentsMargins(12,12,12,12)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setObjectName('cancel')
        cancel_btn.setFixedSize(94, 40)
        cancel_btn.setCursor(qt.CursorShape.PointingHandCursor)
        effect = DropShadowEffect(color=QColor(166, 166, 166, 50), blur_radius=3, dy_offset=3)
        effect.apply(cancel_btn, always_enable=True)

        cancel_btn.clicked.connect(self.close) # Connect button click to closing dialog

        save_btn = QPushButton('Save')
        save_btn.setObjectName('save')
        save_btn.setFixedSize(80, 40)
        save_btn.setCursor(qt.CursorShape.PointingHandCursor)

        self.bottom_bar.addWidget(cancel_btn, alignment=qt.AlignmentFlag.AlignLeft)
        self.bottom_bar.addWidget(save_btn, alignment=qt.AlignmentFlag.AlignRight)

        layout.addWidget(bottom_bar_container)

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