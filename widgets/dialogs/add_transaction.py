from .dialog import FramelessDialog
from PyQt6.QtCore import Qt as qt, QSize
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QDoubleValidator, QValidator, QIcon, QColor
from widgets.components.input import Input
from widgets.components.combobox import ComboBox
from widgets.util.drop_shadow import DropShadowEffect
from widgets.layouts.flowlayout import FlowLayout
from widgets.util.style_util import load_stylesheet
from models.tag import Tag, TagManager

class TransactionDialog(FramelessDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent, 'Add Transaction', 600, 750)

        description_input = Input('Description', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Description').build()
        description_input.setAlignment(qt.AlignmentFlag.AlignTop)

        amount_input = Input('Amount', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Amount')
        amount_input.setAlignment(qt.AlignmentFlag.AlignTop)
        self.amount_textbox = amount_input.get_textbox()

        self.amount_textbox.textChanged.connect(self._on_text_changed)
        self.amount_textbox.cursorPositionChanged.connect(self._on_cursor_position_changed)

        # Layout for tags (label, combobox)
        tag_layout = QVBoxLayout()
        tag_layout.setSpacing(0)
        tag_label = QLabel('Select tags')
        tag_label.setStyleSheet(
            load_stylesheet('styles/components/input.qss') # Re-use qlabel style from input component
            + 'QLabel { padding-bottom: 7px; }'
        )
        
        tag_combobox = ComboBox('Select tags', self.total_width(), 56, effect=DropShadowEffect())

        # Flow layout

        flow_container = QFrame()
        flow_container.setObjectName('container')
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
        flow_layout.setContentsMargins(20,20,20,20)

        flow_container.setFixedWidth(self.total_width()-8)
        flow_container.setLayout(flow_layout)

        tm = TagManager()
        for i in range(0,5):
            flow_layout.addWidget(self.create_tag(tm.all()[i]))

        tag_layout.addWidget(tag_label, alignment=qt.AlignmentFlag.AlignLeft)
        tag_layout.addWidget(tag_combobox, alignment=qt.AlignmentFlag.AlignHCenter)

        self.container.setSpacing(25)

        self.container.addLayout(description_input)
        self.container.addLayout(amount_input.build())
        self.container.addLayout(tag_layout)

        self.container.addWidget(flow_container, alignment=qt.AlignmentFlag.AlignHCenter)
        self.container.addStretch()

    def create_tag(self, tag: Tag) -> QFrame:
        """
        Creates a tag frame to be added to the flow layout
        """

        fg = tag.foreground

        container = QFrame()
        container.setFixedHeight(44)
        container.setContentsMargins(4,0,2,0)
        container.setStyleSheet(
            f'''
            QFrame {{
                border-radius: {44//2}px;
                border: 1px solid #D3D3D3;
            }}
            '''
        )

        layout = QHBoxLayout()
        layout.setSpacing(0)

        dot = QWidget(container)  
        dot.setFixedSize(12,12)
        dot.setStyleSheet(
            f'''
            QWidget {{
                background-color: {fg.name()};
                border-radius: 6px;
            }}
            '''
        )

        dropshadow = DropShadowEffect(QColor(211,211,211,200), blur_radius=20)
        dropshadow.apply(parent=container, always_enable=True)

        label = QLabel(' ' + tag.text)
        label.setContentsMargins(6,3,6,3)
        label.setStyleSheet(
            f'''
            font-family: 'Inter Regular';
            font-size: 19px;
            color: black;
            border: none;
            '''
        )

        btn = QPushButton()
        btn.setIcon(QIcon('assets/icons/x.png'))
        btn.setIconSize(QSize(24,24))
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

    def _on_cursor_position_changed(self, old, new) -> None:
        if new < 2:
            self.amount_textbox.setCursorPosition(2)

    def _on_text_changed(self, text: str) -> None:
        tb = self.amount_textbox

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