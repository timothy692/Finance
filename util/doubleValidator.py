from PyQt6.QtGui import QDoubleValidator, QValidator
from PyQt6.QtWidgets import QLineEdit

class DoubleValidator:
    def __init__(self, currency: str, bottom: float = 0.01, top: float = 999999.99, decimals: int = 2):
        self.bottom = bottom
        self.top = top
        self.decimals = decimals
        self.currency = currency
        self.validator = QDoubleValidator(self.bottom, self.top, self.decimals)
        self.textbox = None 

    def attach(self, textbox: QLineEdit):
        """
        Attach the validator to a specific QLineEdit.
        """
        self.textbox = textbox

        # Disconnect any previous connection
        try:
            self.textbox.textChanged.disconnect()
        except Exception:
            pass

        textbox.textChanged.connect(self._on_text_changed)
        textbox.cursorPositionChanged.connect(self._on_cursor_position_changed)

    def validate(self, text: str) -> str:
        if text.startswith(self.currency):
            text = text[len(self.currency):].strip()

        if 'e' in text:
            text = text.replace('e', '')

        if ',' in text:
            text = text.replace(',', '')

        validator = QDoubleValidator(self.bottom, self.top, self.decimals)
        state, _, _ = validator.validate(text, 0)

        valid_str = ''
        if state == QValidator.State.Acceptable:
            valid_str = text            
        elif state == QValidator.State.Intermediate and text.startswith('0'):
            valid_str = text
        elif state == QValidator.State.Invalid:
            valid_str = text[:-1]

        if state == QValidator.State.Intermediate or state == QValidator.State.Acceptable:
            # if len(text) == 0:
            #     self.textbox.clear()

            try:
                n = float(text)

                if n >= self.top:
                    valid_str = text[:-1]
                elif text.startswith('0') and len(text) > 1 and not text.startswith('0.'):
                    valid_str = str(int(n))
            except ValueError:
                pass        

        return valid_str

    def _on_text_changed(self, text: str) -> None:
        if not self.textbox:
            return

        self.textbox.textChanged.disconnect(self._on_text_changed)

        validated = self.validate(text)
        if len(validated) == 0:
            self.textbox.clear()

        if len(validated) > 0:
            self.textbox.setText(f'{self.currency} {validated}')

        self.textbox.textChanged.connect(self._on_text_changed)

    def _on_cursor_position_changed(self, _, new: int) -> None:
        if not self.textbox:
            return

        if new < len(self.currency) + 1:
            self.textbox.setCursorPosition(len(self.currency)+1)