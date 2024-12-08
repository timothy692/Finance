from .dialog import FramelessDialog
from PyQt6.QtCore import Qt as qt, QEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QDoubleValidator, QValidator
from widgets.components.input import Input
from widgets.components.combobox import ComboBox
from widgets.util.drop_shadow import DropShadowEffect

class TransactionDialog(FramelessDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent, 'Add Transaction', 540, 750)

        description_input = Input('Description', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Description').build()
        description_input.setAlignment(qt.AlignmentFlag.AlignTop)

        amount_input = Input('Amount', self.total_width(), effect=DropShadowEffect()) \
                            .add_input_label('Amount')
        amount_input.setAlignment(qt.AlignmentFlag.AlignTop)
        self.amount_textbox = amount_input.get_textbox()

        self.amount_textbox.textChanged.connect(self._on_text_changed)
        self.amount_textbox.cursorPositionChanged.connect(self._on_cursor_position_changed)

        tag_layout = QHBoxLayout()
        tag_combobox = ComboBox('Select tags', self.total_width(), 57, effect=DropShadowEffect())
        tag_combobox.addItems(['Test1', 'Test2', 'Test3'])
        tag_layout.addWidget(tag_combobox, alignment=qt.AlignmentFlag.AlignLeft)

        self.container.setSpacing(25)

        self.container.addLayout(description_input)
        self.container.addLayout(amount_input.build())
        self.container.addLayout(tag_layout)
        self.container.addStretch()

        # Transaction, Amount, Tags, Account?

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