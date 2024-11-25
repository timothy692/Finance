from pages.page import Page
from widgets.panel import PanelWidget
from PyQt6.QtCore import Qt as qt
from PyQt6.QtCore import QSize, QAbstractTableModel
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QIcon, QColor
from util.style_util import load_stylesheet
from widgets.transaction_treeview import TransactionTreeview
from widgets.transaction_dialog import TransactionDialog
from models.tag import Tag

class TransactionsPage(Page):
    def __init__(self):
        super().__init__()

        self.layout().addStretch()

    def show_transaction_dialog(self) -> None:
        dialog = TransactionDialog()
        if dialog.exec():
            print('exec')

    def _init_top_container(self) -> None:
        def create_button(label: str, object_name: str, width: int, icon: str=None) -> QPushButton:
            btn = QPushButton(label)
            btn.setObjectName(object_name)
            btn.setFixedSize(width, 48)

            if icon:
                btn.setIcon(QIcon(icon))
                btn.setIconSize(QSize(30,30))

            return btn
        
        transactions_btn = create_button(
            'Add transaction', 'transaction', 235
        )

        export_btn = create_button(
            '  Export CSV', 'export', 210, 'assets/export.png'
        )

        import_btn = create_button(
            '  Import CSV', 'import', 210, 'assets/import.png'
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

        tags = {
            'basic': Tag(text="Basic", background_color=QColor(224, 247, 255, 150), text_color=QColor("#1F509A")),
            'must-have': Tag(text="Must have", background_color=QColor("#FFE0E0"), text_color=QColor("#AF1740")),
            'income': Tag(text="Income", background_color=QColor("#E8F5E9"), text_color=QColor("#2E7D32")),
            'sport': Tag(text="Sport", background_color=QColor("#F5E0FF"), text_color=QColor("#7B1FA2")),
            'health': Tag(text="Health", background_color=QColor("#E0F7FF"), text_color=QColor("#017B92")),
            'food': Tag(text="Food", background_color=QColor("#F5F5F5"), text_color=QColor("#545454")),
            'entertainment': Tag(text="Entertainment", background_color=QColor("#FFF2E0"), text_color=QColor("#BF360C")),
        }

        treeview = TransactionTreeview(tags.values())

        treeview.setStyleSheet(
            load_stylesheet('styles/treeview.qss')
        )

        treeview.add_entry(
            ["19.02.2024", "New Transaction", 42, [tags.get('entertainment'), tags.get('income')], "New Account"],
        )

        treeview.add_entry(
            ["19.10.2024", "New Transaction", -90, [tags.get('basic')], "New Account"]
        )

        treeview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_bottom.addWidget(treeview)

