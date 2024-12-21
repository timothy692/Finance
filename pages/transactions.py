from PyQt6.QtCore import QAbstractTableModel, QSize
from PyQt6.QtCore import Qt as qt
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import *

from models.tag import TagManager
from pages.page import Page
from widgets.dialogs.addTransaction import TransactionDialog
from widgets.panel import PanelWidget
from widgets.transactionTreeview import TransactionTreeview
from widgets.util.styleUtil import load_stylesheet


class TransactionsPage(Page):
    def __init__(self):
        super().__init__()

        self.layout().addStretch()

    def show_transaction_dialog(self) -> None:
        dialog = TransactionDialog(self)
        dialog.center()

        dialog.exec()

    def _init_top_container(self) -> None:
        def create_button(label: str, object_name: str, width: int, icon: str=None) -> QPushButton:
            btn = QPushButton(label)
            btn.setObjectName(object_name)
            btn.setFixedSize(width, 48)
            btn.setCursor(qt.CursorShape.PointingHandCursor)

            if icon:
                btn.setIcon(QIcon(icon))
                btn.setIconSize(QSize(30,30))

            return btn
        
        transactions_btn = create_button(
            'Add transaction', 'transaction', 235
        )

        export_btn = create_button(
            '  Export CSV', 'export', 210, 'assets/icons/export.png'
        )

        import_btn = create_button(
            '  Import CSV', 'import', 210, 'assets/icons/import.png'
        )

        self.layout_top.addWidget(import_btn, alignment=qt.AlignmentFlag.AlignLeft)
        self.layout_top.addWidget(export_btn, alignment=qt.AlignmentFlag.AlignLeft)
        self.layout_top.addWidget(transactions_btn, alignment=qt.AlignmentFlag.AlignLeft)

        transactions_btn.clicked.connect(self.show_transaction_dialog)

    def _init_bottom_container(self) -> None:
        # Summary panels

        panel_container = QWidget()
        panel_layout = QHBoxLayout(panel_container)
        panel_layout.setContentsMargins(0,0,0,0)
        panel_layout.setSpacing(25)

        panel_layout.addWidget(
            PanelWidget('Total income', 10000), stretch=1
        )

        panel_layout.addWidget(
            PanelWidget('Total spending', 10000), stretch=1
        )

        panel_layout.addWidget(
            PanelWidget('Net income', 10000), stretch=1
        )

        panel_layout.addStretch()
        panel_container.setLayout(panel_layout)
        self.layout_bottom.addWidget(panel_container)

        # Transaction treeview

        treeview = TransactionTreeview([]) # TODO: add tags

        treeview.setStyleSheet(
            load_stylesheet('styles/treeview.qss')
        )

        # treeview.add_entry(
        #     ["19.02.2024", "New Transaction", 42, [self.tags.get('entertainment'), self.tags.get('income')], "New Account"],
        # )

        # treeview.add_entry(
        #     ["19.10.2024", "New Transaction", -90, [self.tags.get('basic')], "New Account"]
        # )

        treeview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_bottom.addWidget(treeview)