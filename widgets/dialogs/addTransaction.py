from typing import List
from datetime import datetime
from functools import partial

from PyQt6.QtGui import QIcon, QColor, QPixmap, QPainter, QFontMetrics
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QRect, QSize, QPoint, QMargins
from PyQt6.QtWidgets import *

from db import database
from models.tag import Tag
from repositories.tagRepo import TagRepository
from util.doubleValidator import DoubleValidator
from widgets.util.styleUtil import load_stylesheet
from widgets.util.dropshadow import DropShadowEffect
from widgets.components.input import Input
from widgets.layouts.flowlayout import FlowLayout
from widgets.components.combobox import ComboBox

from .dialog import FramelessDialog


class TransactionDialog(FramelessDialog):
    def __init__(self, parent):
        self._selector_menu = QMenu()
        self._selector_menu.setStyleSheet(
            '''
            QMenu {
                background-color: white;
                border: 1px solid #c6c6c6;
                border-radius: 10px;
                padding: 5px;
            }

            QMenu::item {
                color: black;
                background-color: transparent;
                font-family: 'Inter Regular';
                font-size: 14px;
                padding-left: 8px;
                height: 26px;
                border-radius: 8px;
            }

            QMenu::item:selected {
                background-color: #f8f8fa; 
                border: none;
                border-radius: 8px;
            }
            '''
        )

        self.max_tags = 4

        self._tags = database.get_repository(TagRepository).fetch_tags()
        self._added_tags: List[Tag] = []

        self.currency = '$'

        super().__init__(parent, 'Add Transaction', 425, 556)

    def init(self):
        self.set_spacing(15)
        self.set_container_margins(QMargins(30,20,30,15))

        self.container.addLayout(self._init_description_input().build())
        self.container.addLayout(self._init_amount_layout())
        self.container.addLayout(self._init_account_input().build())
        self.container.addLayout(self._init_tag_layout(), stretch=1)

        self.reposition_selector()

        self.container.addStretch()
    
    def on_save(self):
        self.add_data('tags', self._added_tags)
        self.add_data('date', datetime.now().strftime('%Y-%m-%d'))         # TODO: add date inut
        self.add_data('amount', 0)

        is_expense = self._collect_data()['transaction-type'].lower() == 'expense'

        if self.amount.get_textbox().text():
            amount = int(self.amount.get_textbox().text().replace(self.currency, '').strip())

            self.add_data('amount', -amount if is_expense else amount)

        return super().on_save()

    def add_tag(self, tag: Tag) -> None:
        frame = self._create_tag_frame(tag) 
        frame.setObjectName(tag.key)
        delete_btn = frame.findChild(QPushButton)

        # Call remove_tag on button click
        delete_btn.clicked.connect(partial(self.remove_tag, tag.key))

        self.flow_layout.addWidget(frame)

        # Remove tag from tag list to prevent duplicates
        self._added_tags.append(tag)

        self.reposition_selector()

    def remove_tag(self, key: str) -> None:
        for idx,item in enumerate(self.flow_layout.all()):
            if item.widget().objectName() == key:
                self.flow_layout.takeAt(idx)

        for idx,tag in enumerate(self._added_tags):
            if tag.key == key:
                self._added_tags.pop(idx)

        self.reposition_selector()

    def reposition_selector(self) -> None:
        # Delete any previous selectors
        for idx,item in enumerate(self.flow_layout.all()):
            if item.widget().objectName() == 'selector':
                self.flow_layout.takeAt(idx)
        
        exceeds_max = len(self._added_tags) >= self.max_tags

        # Only add selector if tag count <= max_tags
        if not exceeds_max:
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
        
        font_metrics = QFontMetrics(self._selector_menu.font())
        longest_width = 0
            
        # Filter out tags that have already been added
        for tag in [item for item in self._tags if item.key not in {tag.key for tag in self._added_tags}]:
            action = self._selector_menu.addAction(tag.text)
            action.setIcon(QIcon(icon_pixmap(tag.foreground, 18, padding=15)))

            action.triggered.connect(lambda checked, i=tag: self.add_tag(i))

            width = font_metrics.horizontalAdvance(tag.text)
            if(width > longest_width):
                longest_width = width

        # Adjust size with based on longest text plus padding
        self._selector_menu.setFixedWidth((longest_width*2) + 35)

        btn = self.sender()
        pos = btn.mapToGlobal(QPoint(0, btn.height()))
        self._selector_menu.exec(pos)

    def _create_selector_frame(self) -> QFrame:
        """
        Creates a selector frame with a child button
        """

        container = QFrame()
        container.setFixedHeight(20)
        container.setContentsMargins(0,0,0,0)

        selector = QPushButton('+')
        selector.setCursor(qt.CursorShape.PointingHandCursor)
        selector.setStyleSheet(
            '''
            QPushButton, QPushButton:hover, QPushButton:pressed {
                background-color: transparent;
                color: black;
                border: none;
                font-family: 'Inter Regular';
                font-size: 22px;
                outline: none;
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
        container.setFixedHeight(33)
        container.setContentsMargins(2,0,0,0)
        container.setStyleSheet(
            '''
            QFrame {
                border-radius: 16px;
                border: 1px solid #D3D3D3;
            }
            '''
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(6,3,6,3)
        layout.setSpacing(0)

        dot = QWidget(container)  
        dot.setFixedSize(8,8)
        dot.setStyleSheet(
            f'''
            QWidget {{
                background-color: {tag.foreground.name()};
                border-radius: 4px;
            }}
            '''
        )

        dropshadow = DropShadowEffect(QColor(211,211,211,200), blur_radius=20)
        dropshadow.apply(parent=container, always_enable=True)

        label = QLabel(' ' + tag.text)
        label.setContentsMargins(3,0,3,0)
        label.setStyleSheet(
            '''
            font-family: 'Inter Regular';
            font-size: 13px;
            color: black;
            border: none;
            '''
        )

        btn = QPushButton()
        btn.setIcon(QIcon('assets/icons/x.png'))
        btn.setProperty('key', tag.key)
        btn.setIconSize(QSize(16,16))
        btn.setCursor(qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            '''
            QPushButton, QPushButton:hover, QPushButton:pressed {
                background-color: transparent;
                color: black;
                border: none;
                outline: none;
            }
            '''
        )

        layout.addWidget(dot, alignment=qt.AlignmentFlag.AlignLeft | qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(label, alignment=qt.AlignmentFlag.AlignHCenter | qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(btn, alignment=qt.AlignmentFlag.AlignRight | qt.AlignmentFlag.AlignVCenter)

        container.setLayout(layout)
        return container

    def _init_description_input(self) -> Input:
        inp = Input('Description', self.container_width(), effect=DropShadowEffect()) \
                            .add_input_label('Description')
        self.register_data_widget('description', inp.get_textbox())

        return inp
    
    def _init_amount_layout(self) -> QVBoxLayout:
        height = 40
        type_width = 103
        total_width = self.container_width()-type_width

        hlayout = QHBoxLayout()
        hlayout.setSpacing(0)
        
        _type = ComboBox(width=type_width, height=height, border_radius=0, effect=DropShadowEffect())
        self.amount = Input(placeholder='Amount', width=total_width, height=height, border_radius=0, effect=DropShadowEffect())
        textbox = self.amount.get_textbox()
        
        self.register_data_widget('transaction-type', _type)

        _type.activated.connect(lambda: textbox.setFocus())

        _type.addItems(['Expense', 'Income'])
        _type.setStyleSheet(
            _type.styleSheet() +
            '''
            QComboBox {
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                border-right: none;
                background-color: #f8f8fa;
            }

            QComboBox::down-arrow, QComboBox::down-arrow:on , QComboBox::drop-down {
                background-color: #f8f8fa;
            }
            '''
        )
        
        textbox.setStyleSheet(
            textbox.styleSheet() +
            '''
            QLineEdit {
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            '''
        )

        self.validator = DoubleValidator(self.currency)
        self.validator.attach(textbox)

        hlayout.addWidget(_type)
        hlayout.addLayout(self.amount.build())

        vlayout = QVBoxLayout()
        vlayout.setSpacing(7)
        label = QLabel('Type and amount')
        label.setStyleSheet(
            load_stylesheet('styles/components/input.qss')
        )

        vlayout.addWidget(label, alignment=qt.AlignmentFlag.AlignTop | qt.AlignmentFlag.AlignLeft)
        vlayout.addLayout(hlayout)

        return vlayout

    def _init_account_input(self) -> Input:
        inp = Input('Account', self.container_width(), effect=DropShadowEffect()) \
                            .add_input_label('Account')
        self.register_data_widget('account', inp.get_textbox())

        return inp

    def _init_tag_layout(self) -> QVBoxLayout:
        tag_layout = QVBoxLayout()
        tag_layout.setSpacing(0)
        tag_layout.setContentsMargins(0,0,0,0)

        tag_label = QLabel('Select tags')
        tag_label.setStyleSheet(
            load_stylesheet('styles/components/input.qss') + # Re-use qlabel style from input component

            '''
            QLabel 
            { 
                padding-bottom: 7px; 
                margin-left: -2px;
            }
            '''
        )
        
        flow_container = QFrame() # Frame for the flow layout to customize border
        flow_container.setObjectName('container')
        flow_container.setFixedWidth(self.container_width())
        flow_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        flow_container.setStyleSheet(
            '''
            QFrame#container {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 12px;   
            }   
            '''
        )

        flow_layout = FlowLayout(hspacing=5, vspacing=5) 
        flow_layout.setGeometry(QRect())
        flow_container.setLayout(flow_layout) # Flow container's layout is set to flow layout

        tag_layout.addWidget(tag_label, alignment=qt.AlignmentFlag.AlignLeft)
        tag_layout.addWidget(flow_container, stretch=1)

        self.flow_layout = flow_layout
        return tag_layout