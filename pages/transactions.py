from datetime import datetime

from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QSize, QAbstractTableModel
from PyQt6.QtWidgets import *

from db import database
from data.csv import CSV
from pages.page import Page
from widgets.panel import PanelWidget
from models.transaction import Transaction
from widgets.util.styleUtil import load_stylesheet
from services.financeService import FinanceService
from widgets.dialogs.importCSV import ImportCSV
from widgets.transactionTreeview import TransactionTreeview
from repositories.transactionRepo import TransactionRepository
from widgets.dialogs.addTransaction import TransactionDialog


class TransactionsPage(Page):
    def __init__(self):
        self._transaction_repo = database.get_repository(TransactionRepository)

        self._finance_service = FinanceService(self._transaction_repo)

        # self._finance_service.load(self._transaction_repo.fetch_transactions())

        # self._transaction_repo.on_update.connect(self.on_emit)

        super().__init__()
        # self.layout().addStretch()

    def show_transaction_dialog(self) -> None:
        dialog = TransactionDialog(self)
        dialog.center()

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            # transaction = Transaction(date=data['date'], description=data['description'], amount=data['amount'],
            #                           balance=data['balance'], account=data['account'], category=data['tags'])

            # self.transactions.add_entry(
            #     ['23.10.2024', data['description'], float(data['amount']), tags, data['account']]
            # )

            # self._transaction_repo.put_transaction(
            #     transaction
            # )

    def show_import_dialog(self) -> None:
        repo = database.get_repository(TransactionRepository)

        csv = CSV()
        csv.import_csv()
        
        data = csv.data()
        repo.put_transactions_many(data)

    def _init_top_container(self) -> None:
        """
        Initialize the top container (buttons)
        """

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
        """
        Initialize the bottom container (panels, treeview)
        """

        panel_container = QWidget()
        panel_layout = QHBoxLayout(panel_container)
        panel_layout.setContentsMargins(0,0,0,0)
        panel_layout.setSpacing(15)

        # year = datetime.now().year
        # curr_month = self._finance_service.total_spending(datetime.now().month, year)
        # last_month = self._finance_service.total_spending((datetime.now().month - 1) or 12, year)

        # panel_layout.addWidget(
        #     PanelWidget('Total income', 10000, 0), stretch=1
        # )

        # panel_layout.addWidget(
        #     PanelWidget('Total spending', 
        #                 curr_month, self._finance_service.difference(curr_month, last_month)
        #     ), stretch=1
        # )

        # panel_layout.addWidget(
        #     PanelWidget('Net income', 10000, 0), stretch=1
        # )

        panel_layout.addStretch()
        panel_container.setLayout(panel_layout)
        self.layout_bottom.addWidget(panel_container)

        self.transactions = TransactionTreeview([]) # TODO: add tags

        self.transactions.setStyleSheet(
            load_stylesheet('styles/treeview.qss')
        )

        self.transactions.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_bottom.addWidget(self.transactions)