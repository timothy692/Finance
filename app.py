import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from util.style_util import load_stylesheet
from pages.transactions import TransactionsPage
from typing import List
from pages.dashboard import DashboardPage

class App(QMainWindow):
    def __init__(self, title: str, width=1600, height=1100) -> None:        
        # Ensure qt is not initialized more than once
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance() 

        super().__init__()

        self.setWindowTitle(title)
        self.setGeometry(100, 100, width, height)

        # Initialize the main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main = QHBoxLayout(main_widget)
        self.main.setContentsMargins(0,0,0,0)
        self.main.setSpacing(0)

        self.buttons: List[QPushButton] = []
        self.page_idx = 1

        self._init_sidebar()
        self._init_container()

    def _on_sidebar_button_clicked(self, idx: int) -> None:
        # Reset all buttons
        for btn in self.buttons:
            btn.setStyleSheet(
                'background-color: transparent;'
            )

        self.buttons[idx].setStyleSheet(
            'background-color: white;'
        )

        self.page_idx = idx
        self._set_page(idx)

    def _set_page(self, idx: int) -> None:
        self._container_stack.setCurrentIndex(idx)

    def _init_sidebar(self):
        frame = QFrame()
        frame.setObjectName('sidebar')
        frame.setFixedWidth(470)
        sidebar = QVBoxLayout(frame)
        sidebar.setContentsMargins(0,0,0,0) # Ensure separator does not have a margin

        sidebar.addSpacing(100) # Spacing from the top
        
        frame.setStyleSheet(
            load_stylesheet('styles/sidebar.qss')
        )

        separator = QFrame()
        separator.setStyleSheet(
            'background-color: #c8c8c8;'
        )
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setFixedWidth(frame.width())
        separator.setFixedHeight(2)
        sidebar.addWidget(separator)

        sidebar.addSpacing(80) # Spacing below the separator

        idx = 0
        def create_button(name: str, icon: str, size: int) -> QPushButton:
            nonlocal idx

            button = QPushButton(' ' * 3 + name)
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(size, size))
            button.setLayoutDirection(qt.LayoutDirection.LeftToRight)
            button.setFixedHeight(90)

            self.buttons.append(button)
            button.clicked.connect(lambda _, index=idx: self._on_sidebar_button_clicked(index))

            idx += 1

            return button
            
        sidebar.addWidget(
            create_button('Dashboard', 'assets/dashboard.png', 48)
        )
        sidebar.addWidget(
            create_button('Transactions', 'assets/transactions.png', 48)
        )
        sidebar.addWidget(
            create_button('Budgets', 'assets/budgets.png', 48)
        )
        sidebar.addWidget(
            create_button('Insights', 'assets/insights.png', 48)
        )
        sidebar.addWidget(
            create_button('Investments', 'assets/investments.png', 48)
        )

        sidebar.addStretch() # Push the buttons to the top
        self.main.addWidget(frame, alignment=qt.AlignmentFlag.AlignLeft)

    def _init_container(self):
        frame = QFrame()
        frame.setObjectName('container')
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) 
        container = QVBoxLayout(frame)
        container.setContentsMargins(0,0,0,0)

        frame.setStyleSheet(
            load_stylesheet('styles/container.qss')
        )

        container_stack = QStackedWidget()
        container_stack.setContentsMargins(0,0,0,0)
        container_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        container_stack.addWidget(DashboardPage())
        container_stack.addWidget(TransactionsPage())
        container.addWidget(container_stack)
        
        # container.addStretch()
        self.main.addWidget(frame, qt.AlignmentFlag.AlignRight)

        self._container_stack = container_stack
        self._on_sidebar_button_clicked(self.page_idx)

    def run(self) -> None:
        self.show()
        sys.exit(self.app.exec())