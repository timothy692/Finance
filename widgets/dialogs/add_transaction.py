from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt as qt
from PyQt6.QtGui import (QColor, QColorConstants, QDoubleValidator, QIcon,
                         QValidator)
from PyQt6.QtWidgets import *

from models.tag import Tag, TagManager
from widgets.components.combobox import ComboBox
from widgets.components.input import Input
from widgets.layouts.flowlayout import FlowLayout
from widgets.util.drop_shadow import DropShadowEffect
from widgets.util.style_util import load_stylesheet

from .dialog import FramelessDialog


class TransactionDialog(FramelessDialog):
    def __init__(self, parent: QWidget):
        self._selector_idx = -1 # Selector index for add item in flow layout
        self._menu_items = None

        super().__init__(parent, 'Add Transaction', 600, 750)

    def init(self):
        self.container.setSpacing(25)

        description_input = Input('Description', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Description').build()

        self.container.addLayout(description_input)

        amount_input = Input('Amount', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Amount')
        
        self.container.addLayout(amount_input.build())

        self._amount_tb = amount_input.get_textbox()
        self._amount_tb.textChanged.connect(self._on_text_changed)
        self._amount_tb.cursorPositionChanged.connect(self._on_cursor_position_changed)

        # Layout for tags (label, flow layout)

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

        self.move_selector(flow_layout)

        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(flow_container)

        self.container.addLayout(tag_layout)
        self.container.addStretch()

    def add_tag(self, tag: Tag, flow_layout: FlowLayout) -> None:
        tag_frame = self._create_tag_frame(tag.text, tag.foreground)
        flow_layout.addWidget(tag_frame)

        self.move_selector(flow_layout) # Move the selector to the end

    def move_selector(self, flow_layout: FlowLayout) -> None:
        if self._selector_idx != -1:
            item = flow_layout.takeAt(self._selector_idx)
            if item and item.widget():
                item.widget().setParent(None) # Remove the old selector visually
        
        # Add the new selector at the end
        selector = self._create_selector_frame()
        flow_layout.addWidget(selector)

        # Attaching the child button to the click event function
        btn = selector.findChild(QPushButton)
        btn.clicked.connect(self._selector_click_event)
        
        # Update the selector index to the new end
        self._selector_idx = flow_layout.count()-1

    def _selector_click_event(self) -> None:
        menu = QMenu()

        menu.addAction()

    def _create_selector_frame(self) -> QFrame:
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

    def _create_tag_frame(self, text: str, foreground: QColor) -> QFrame:
        """
        Creates a tag frame to be added to the flow layout
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
                background-color: {foreground.name()};
                border-radius: 6px;
            }}
            '''
        )

        dropshadow = DropShadowEffect(QColor(211,211,211,200), blur_radius=20)
        dropshadow.apply(parent=container, always_enable=True)

        label = QLabel(' ' + text)
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