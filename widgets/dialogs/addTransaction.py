from typing import Dict, List
from functools import partial

from PyQt6.QtGui import QIcon, QColor, QPixmap, QPainter, QValidator,  QDoubleValidator
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
        self._last_selector_idx = -1 # Selector index for add item in flow layout
        self._added_tags: Dict[str, int] = dict()

        self._tag_menu = QMenu()
        self._tag_menu.setFixedWidth(300)

        self._tag_menu.setStyleSheet(
            '''
            QMenu {
                background-color: white;
                border: 1px solid #c6c6c6;
                border-radius: 16px;
                padding: 8px;
            }

            QMenu::item {
                color: black;
                background-color: transparent;
                font-family: 'Inter Regular';
                font-size: 21px;
                padding-left: 20px;
                height: 40px;
                border-radius: 8px;
            }

            QMenu::item:selected {
                background-color: #f8f8fa; 
                border: none;
                border-radius: 8px;
            }
            '''
        )
        self._tags = TagManager().all()

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
        self.flow_layout = FlowLayout() 
        flow_container.setLayout(self.flow_layout) # Flow container's layout is set to flow layout

        self.move_selector()

        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(flow_container)

        self.container.addLayout(tag_layout)
        self.container.addStretch()

    def add_tag(self, tag: Tag) -> None:
        tag_frame = self._create_tag_frame(tag.text, tag.foreground)
        btn = tag_frame.findChild(QPushButton)

        idx = self.flow_layout.count()  # Current count before adding the tag
        self._added_tags[btn.objectName()] = idx
        btn.clicked.connect(partial(self._handle_tag_click, idx))

        self.flow_layout.addWidget(tag_frame)

        print(f'Added tag, moving selector to idx {idx + 1}')
        self.move_selector()


        print('added tag, moved selector from idx',self._last_selector_idx,'to',idx+1)
        self.move_selector(self._last_selector_idx, idx+1) 

    def move_selector(self) -> None:
        # Remove the existing selector if it exists
        if self._last_selector_idx != -1:
            item = self.flow_layout.takeAt(self._last_selector_idx)
            if item and item.widget():
                item.widget().setParent(None)

        # Add the selector at the end
        selector = self._create_selector_frame()
        self.flow_layout.addWidget(selector)

        btn = selector.findChild(QPushButton)
        btn.co

        # Update the selector index to the last position
        self._last_selector_idx = self.flow_layout.count() - 1
        print(f'Moved selector to idx {self._last_selector_idx}')
                
    def _selector_menu(self) -> None:
        if len(self._tag_menu.actions()) > 0:
            self._tag_menu.clear()

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
        
        for item in self._tags:
            action = self._tag_menu.addAction(item.text)
            action.setIcon(QIcon(icon_pixmap(item.foreground, 18, padding=15)))

            action.triggered.connect(lambda checked, t=item.text: self._handle_menu_click(t))

        btn = self.sender()
        pos = btn.mapToGlobal(QPoint(0, btn.height()))
        self._tag_menu.exec(pos)
    
    def _handle_menu_click(self, text: str) -> None:
        for item in self._tags:
            if item.text == text:
                # Remove the tag from the tag list to prevent duplicate tags
                self._tags.remove(item)   

                # Add the tag to the flow layout
                self.add_tag(item)

    def _handle_tag_click(self, index: int) -> None:
        # Remove the tag widget at the given index
        item = self.flow_layout.takeAt(index)
        if item and item.widget():
            item.widget().setParent(None)

        # Update `_added_tags` to reflect the removal
        tag_to_remove = None
        for tag, idx in self._added_tags.items():
            if idx == index:
                tag_to_remove = tag
                break

        if tag_to_remove:
            del self._added_tags[tag_to_remove]

        # Shift the indices of remaining tags
        for tag, idx in self._added_tags.items():
            if idx > index:
                self._added_tags[tag] = idx - 1

        # Reposition the selector
        print(f'Removed tag at idx {index}, repositioning selector')
        self.move_selector()

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

    def _create_tag_frame(self, tag: Tag) -> QFrame:
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