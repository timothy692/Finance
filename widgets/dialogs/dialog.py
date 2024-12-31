from PyQt6.QtCore import QPoint, QSize, QMargins
from PyQt6.QtCore import Qt as qt
from PyQt6.QtGui import QColor, QIcon, QPixmap
from PyQt6.QtWidgets import *

from widgets.components.separator import Separator
from widgets.util.dropshadow import DropShadowEffect
from widgets.util.styleUtil import load_stylesheet
from typing import Dict


class FramelessDialog(QDialog):
    def __init__(self, parent: QWidget, title: str, width: int, height: int):
        super().__init__(parent)

        self.setWindowFlags(
            qt.WindowType.FramelessWindowHint | qt.WindowType.Window
        )

        self.title = title
        self.setModal(True)
        self.setFixedSize(width, height)

        self.setStyleSheet(
            load_stylesheet('styles/dialog.qss')
        )

        self._margins = QMargins(30,30,30,30)

        self._registered_widgets = {}
        self._data = {}

        self._init_gui()
        self.init()
    
    def _init_gui(self) -> None:
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # Top bar

        self.top_bar = QHBoxLayout()
        self.top_bar.setContentsMargins(20,15,20,6)
        
        title = QLabel(self.title)
        title.setObjectName('title')
        
        close = QPushButton()
        close.setCursor(qt.CursorShape.PointingHandCursor)
        close.setIcon(QIcon(
            QPixmap('assets/icons/close.png').scaled(16, 16, 
                                              qt.AspectRatioMode.KeepAspectRatio,
                                              qt.TransformationMode.SmoothTransformation)
        ))

        close.setStyleSheet(
            '''
            background-color: transparent; 
            border: none;
            outline: none;
            '''
        )

        close.clicked.connect(self.close)

        self.top_bar.addStretch()
        self.top_bar.addWidget(title, alignment=qt.AlignmentFlag.AlignCenter)
        self.top_bar.addStretch()
        self.top_bar.addWidget(close, alignment=qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(self.top_bar)
        layout.addWidget(Separator(QColor(200,200,200)))

        self.container = QVBoxLayout()
        self.container.setContentsMargins(self._margins)
        self.container.setSpacing(0)
        self.container.addStretch()

        layout.addLayout(self.container, stretch=1)

        bottom_bar_container = QWidget(self)
        bottom_bar_container.setObjectName('bottom-bar')

        self.bottom_bar = QHBoxLayout(bottom_bar_container)
        self.bottom_bar.setContentsMargins(12,9,12,9)

        cancel_btn = QPushButton('Cancel')
        cancel_btn.setObjectName('cancel')
        cancel_btn.setFixedSize(70, 35)
        cancel_btn.setCursor(qt.CursorShape.PointingHandCursor)
        effect = DropShadowEffect(color=QColor(166, 166, 166, 50), blur_radius=3, dy_offset=3)
        effect.apply(cancel_btn, always_enable=True)

        cancel_btn.clicked.connect(self.on_cancel) # Connect button click to closing dialog

        save_btn = QPushButton('Save')
        save_btn.setObjectName('save')
        save_btn.setFixedSize(55, 35)
        save_btn.setCursor(qt.CursorShape.PointingHandCursor)

        save_btn.clicked.connect(self.on_save)

        self.bottom_bar.addWidget(cancel_btn, alignment=qt.AlignmentFlag.AlignLeft)
        self.bottom_bar.addWidget(save_btn, alignment=qt.AlignmentFlag.AlignRight)

        layout.addWidget(bottom_bar_container)

        self.setLayout(layout)

    def register_data_widget(self, key: str, widget: QWidget) -> None:
        self._registered_widgets[key] = widget

    def add_data(self, key: str, data: any) -> None:
        self._data[key] = data

    def _collect_data(self) -> dict[str, any]:
        data = {}

        for k,w in self._registered_widgets.items():
            value = None

            if isinstance(w, QLineEdit):
                value = w.text()
            elif isinstance(w, QComboBox):
                value = w.currentText()

            data[k] = value

        return data

    def validate_data(self) -> bool:
        """
        If any data is missing, False is returned
        """

        valid = True

        for value in self._data.values():
            if not value or (isinstance(value, str) and len(value) == 0):
                valid = False

        return valid
            
    def get_data(self) -> Dict[str, any]:
        return self._data

    def init(self) -> None: 
        """
        Initialize the content of the dialog
        """
        
        pass

    def on_cancel(self) -> None:
        """
        Called when the cancel button is pressed
        """

        self.reject()

    def on_save(self) -> None:
        """
        Called when the save button is pressed
        """

        for k,v in self._collect_data().items():
            self._data[k] = v

        if self.validate_data():
            self.accept()

    def container_width(self) -> int:
        return (self.width() - self._margins.left()) - self._margins.right()
    
    def set_spacing(self, spacing: int) -> None:
        self.container.setSpacing(spacing)

    def set_container_margins(self, margins: QMargins) -> None:
        self.container.setContentsMargins(margins)
        self._margins = margins
    
    def create_widget_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName('widget-label')
        label.setFixedHeight(25)
        return label

    def center(self):
        """
        Center the dialog inside the app
        """

        if self.parent():
            parent_geometry = self.parent().geometry()
            dialog_geometry = self.frameGeometry()
            dialog_geometry.moveCenter(parent_geometry.center())
            self.move(dialog_geometry.topLeft())

    def keyPressEvent(self, event):
        """
        Disable key event for closing dialog
        """

        if event.key() == qt.Key.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)