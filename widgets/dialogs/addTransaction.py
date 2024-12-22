from typing import Dict, List
from functools import partial

from PyQt6.QtGui import QIcon, QColor, QPixmap, QPainter, QValidator, QDoubleValidator
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QSize, QPoint
from PyQt6.QtWidgets import *

from models.tag import Tag, TagManager
from widgets.util.styleUtil import load_stylesheet
from widgets.util.dropshadow import DropShadowEffect
from widgets.components.input import Input
from widgets.layouts.flowlayout import FlowLayout
from widgets.components.combobox import ComboBox

from .dialog import FramelessDialog


class TransactionDialog(FramelessDialog):
    def __init__(self, parent: QWidget):
        self._selector_menu = QMenu()
        self._tags: List[str] = []

        super().__init__(parent, 'Add Transaction', 600, 750)

    def init(self):
        self.spacing(25)

        self.container.addLayout(self._init_description_input().build())
        self.container.addLayout(self._init_amount_input().build())
        self.container.addLayout(self._init_tag_layout())

        self.reposition_selector()

        self.container.addStretch()

    def add_tag(self, tag: Tag) -> None:
        self.flow_layout.parentWidget().setUpdatesEnabled(False)

        frame = self._create_tag_frame(tag) 
        frame.setObjectName(tag.key)
        delete_btn = frame.findChild(QPushButton)

        # Call remove_tag on button click 
        delete_btn.clicked.connect(partial(self.remove_tag, tag.key))

        self.flow_layout.addWidget(frame)
        self.reposition_selector()

        self.flow_layout.parentWidget().setUpdatesEnabled(True)

    def remove_tag(self, key: str) -> None:
        for idx,item in enumerate(self.flow_layout.all()):
            if item.widget().objectName() == key:
                self.flow_layout.takeAt(idx)

    def reposition_selector(self) -> None:
        # Delete any previous selectors
        for idx,item in enumerate(self.flow_layout.all()):
            if item.widget().objectName() == 'selector':
                self.flow_layout.takeAt(idx)
                print('removed selector at',idx)

        frame = self._create_selector_frame()
        frame.setObjectName('selector')

        selector_btn = frame.findChild(QPushButton)
        selector_btn.clicked.connect(self._show_selector_menu)

        self.flow_layout.addWidget(frame)

    def _show_selector_menu(self) -> None:
        if len(self._selector_menu.actions()) > 0:
            self._selector_menu.clear()

        def icon_pixmap(color: str, size: int, padding: int) -> QPixmap:
            """
            Create a QPixmap with a colored dot
            """

            pixmap = QPixmap(size + padding, size) # Horizontal padding
            pixmap.fill(QColor(0, 0, 0, 0))

            painter = QPainter(pixmap)
            painter.setBrush(QColor(color))
            painter.setPen(qt.PenStyle.NoPen)

            # Draw the dot shifted to the right
            painter.drawEllipse(padding, 0, size, size)
            painter.end()

            return pixmap
        
        tag_manager = TagManager()
        
        for item in tag_manager.all():
            action = self._selector_menu.addAction(item.text)
            action.setIcon(QIcon(icon_pixmap(item.foreground, 18, padding=15)))

            # action.triggered.connect(lambda checked, t=item.text: self._handle_menu_click(t))
            action.triggered.connect(lambda checked, i=item: self.add_tag(i))

        btn = self.sender()
        pos = btn.mapToGlobal(QPoint(0, btn.height()))
        self._selector_menu.exec(pos)

    def _create_selector_frame(self) -> QFrame:
        """
        Creates a selector frame with a child button
        """

        container = QFrame()
        container.setFixedHeight(25)
        container.setContentsMargins(0,3,0,0)

        selector = QPushButton('+')
        selector.setCursor(qt.CursorShape.PointingHandCursor)
        selector.setStyleSheet(
            '''
            QPushButton, QPushButton:hover, QPushButton:pressed {
                background-color: transparent;
                color: black;
                border: none;
                font-family: 'Inter Regular';
                font-size: 30px;
            }
            '''
        )

        layout = QHBoxLayout(container)
        layout.addWidget(selector)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(selector, qt.AlignmentFlag.AlignVCenter | qt.AlignmentFlag.AlignHCenter)

        return container

    def _create_tag_frame(self, tag: Tag) -> QFrame:
        """
        Creates a tag frame with a child button
        """

        container = QFrame()
        container.setFixedHeight(44)
        container.setContentsMargins(4,0,2,0)
        container.setStyleSheet(
            '''
            QFrame {
                border-radius: 22px;
                border: 1px solid #D3D3D3;
            }
            '''
        )

        layout = QHBoxLayout()
        layout.setSpacing(0)

        dot = QWidget(container)  
        dot.setFixedSize(12,12)
        dot.setStyleSheet(
            f'''
            QWidget {{
                background-color: {tag.foreground.name()};
                border-radius: 6px;
            }}
            '''
        )

        dropshadow = DropShadowEffect(QColor(211,211,211,200), blur_radius=20)
        dropshadow.apply(parent=container, always_enable=True)

        label = QLabel(' ' + tag.text)
        label.setContentsMargins(6,3,6,3)
        label.setStyleSheet(
            '''
            font-family: 'Inter Regular';
            font-size: 19px;
            color: black;
            border: none;
            '''
        )

        btn = QPushButton()
        btn.setIcon(QIcon('assets/icons/x.png'))
        btn.setProperty('key', tag.key)
        btn.setIconSize(QSize(24,24))
        btn.setCursor(qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            '''
            QPushButton, QPushButton:hover, QPushButton:pressed {
                background-color: transparent;
                color: black;
                border: none;
            }
            '''
        )

        layout.addWidget(dot, alignment=qt.AlignmentFlag.AlignLeft | qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(label, alignment=qt.AlignmentFlag.AlignLeft)
        layout.addWidget(btn, alignment=qt.AlignmentFlag.AlignRight | qt.AlignmentFlag.AlignTop)

        container.setLayout(layout)
        return container

    def _init_description_input(self) -> Input:
        return Input('Description', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Description')
    
    def _init_amount_input(self) -> Input:
        amount_input = Input('Amount', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Amount')
        
        self._amount_tb = amount_input.get_textbox()
        self._amount_tb.textChanged.connect(self._on_text_changed)
        self._amount_tb.cursorPositionChanged.connect(self._on_cursor_position_changed)

        return amount_input

    def _init_tag_layout(self) -> QVBoxLayout:
        tag_layout = QVBoxLayout()
        tag_layout.setSpacing(0)

        tag_label = QLabel('Select tags')
        tag_label.setStyleSheet(
            load_stylesheet('styles/components/input.qss') + # Re-use qlabel style from input component

            '''
            QLabel 
            { 
                padding-bottom: 7px; 
            }
            '''
        )
        
        flow_container = QFrame() # Frame for the flow layout to customize border
        flow_container.setObjectName('container')
        flow_container.setFixedWidth(self.total_width()-8)
        flow_container.setStyleSheet(
            '''
            QFrame#container {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 10px;   
            }   
            '''
        )

        flow_layout = FlowLayout() 
        flow_container.setLayout(flow_layout) # Flow container's layout is set to flow layout

        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(flow_container)

        self.flow_layout = flow_layout
        return tag_layout

    def _on_cursor_position_changed(self, _, new) -> None:
        if new < 2:
            self._amount_tb.setCursorPosition(2)

    def _on_text_changed(self, text: str) -> None:
        """
        Amount validator logic
        """

        tb = self._amount_tb

        tb.textChanged.disconnect(self._on_text_changed)

        if text.startswith('$'):
            text = text[1:].strip()

        if 'e' in text:
            text = text.replace('e', '')
        
        if ',' in text:
            text = text.replace(',', '')

        bottom = 0.01
        top = 999999.99

        validator = QDoubleValidator(bottom, top, 2)
        state,_,_ = validator.validate(text, 0)

        valid_str = ''
        if state == QValidator.State.Acceptable:
            valid_str = text            
        elif state == QValidator.State.Intermediate and text.startswith('0'):
            valid_str = text
        elif state == QValidator.State.Invalid:
            valid_str = text[:-1]

        if state == QValidator.State.Intermediate or state == QValidator.State.Acceptable:
            if len(text) == 0:
                tb.clear()

            try:
                n = float(text)

                if n >= top:
                    valid_str = text[:-1]
                elif text.startswith('0') and len(text) > 1 and not text.startswith('0.'):
                    valid_str = str(int(n))
            except ValueError:
                pass
        
        if len(text) > 0:
            tb.setText(f'$ {valid_str}')

        tb.textChanged.connect(self._on_text_changed)