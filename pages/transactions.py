from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QSize, QAbstractTableModel
from PyQt6.QtWidgets import *

from data.csv import CSV
from pages.page import Page
from widgets.panel import PanelWidget
from widgets.util.styleUtil import load_stylesheet
from widgets.dialogs.importCSV import ImportCSV
from widgets.transactionTreeview import TransactionTreeview
from widgets.dialogs.addTransaction import TransactionDialog


class TransactionsPage(Page):
    def __init__(self):
        super().__init__()

        self.layout().addStretch()

    def show_transaction_dialog(self) -> None:
        dialog = TransactionDialog(self)
        dialog.center()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            tags = data['tags']
            
            self.transactions.add_entry(
                ['23.10.2024', data['description'], float(data['amount']), tags, data['account']]
            )

    def show_import_dialog(self) -> None:
        # dialog = ImportCSV(self)
        # dialog.center()

        # dialog.exec()
        data = CSV().import_csv()
        print(data)

    def _init_top_container(self) -> None:
        def create_button(label: str, object_name: str, width: int, icon: str=None) -> QPushButton:
            btn = QPushButton(label)
            btn.setObjectName(object_name)
            btn.setFixedSize(width, 32)
            btn.setCursor(qt.CursorShape.PointingHandCursor)

            if icon:
                btn.setIcon(QIcon(icon))
                btn.setIconSize(QSize(19,19))

            return btn
        
        transactions_btn = create_button(
            'Add transaction', 'transaction', 155
        )

        export_btn = create_button(
            '  Export CSV', 'export', 146, 'assets/icons/export.png'
        )

        import_btn = create_button(
            '  Import CSV', 'import', 146, 'assets/icons/import.png'
        )

        self.layout_top.addWidget(import_btn, alignment=qt.AlignmentFlag.AlignLeft)
        self.layout_top.addWidget(export_btn, alignment=qt.AlignmentFlag.AlignLeft)
        self.layout_top.addWidget(transactions_btn, alignment=qt.AlignmentFlag.AlignLeft)

        transactions_btn.clicked.connect(self.show_transaction_dialog)
        import_btn.clicked.connect(self.show_import_dialog)

    def _init_bottom_container(self) -> None:
        # Summary panels

        panel_container = QWidget()
        panel_layout = QHBoxLayout(panel_container)
        panel_layout.setContentsMargins(0,0,0,0)
        panel_layout.setSpacing(15)

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

        self.transactions = TransactionTreeview([]) # TODO: add tags

        self.transactions.setStyleSheet(
            load_stylesheet('styles/treeview.qss')
        )

        # self.transactions.add_entry(
        #     ['23.10.2024', 'Description', 19.99, TagManager().get_tag('basic'), 'Credit Card']
        # )

        # self.transactions.add_entry(
        #     ['23.10.2024', 'Description', 19.99, [TagManager().get_tag('must-have'), TagManager().get_tag('entertainment')], 'Credit Card']
        # )

        self.transactions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_bottom.addWidget(self.transactions)