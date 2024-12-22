from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import QObject


class DoubleValidator(QObject):
    def __init__(self, textbox: QLineEdit, min_value=0.01, max_value=999999.99, decimals=2):
        super().__init__()
        self.textbox = textbox
        self.min_value = min_value
        self.max_value = max_value
        self.decimals = decimals

        # Initialize the validator
        self.validator = QDoubleValidator(self.min_value, self.max_value, self.decimals)

        # Connect the textChanged signal to the handler
        self.textbox.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self, text: str) -> None:
        """
        Validate and format the input text.
        """
        self.textbox.textChanged.disconnect(self._on_text_changed)

        # Strip unwanted characters
        text = self._sanitize_input(text)

        # Validate and format the input
        formatted_text = self._validate_and_format(text)

        # Update the textbox
        if formatted_text:
            self.textbox.setText(f"$ {formatted_text}")
        else:
            self.textbox.clear()

        self.textbox.textChanged.connect(self._on_text_changed)

    def _sanitize_input(self, text: str) -> str:
        """
        Remove unwanted characters like '$', 'e', and ','.
        """
        if text.startswith('$'):
            text = text[1:].strip()
        return text.replace('e', '').replace(',', '')

    def _validate_and_format(self, text: str) -> str:
        """
        Validate the input text and format it appropriately.
        """
        state, _, _ = self.validator.validate(text, 0)

        if state == QDoubleValidator.State.Acceptable:
            return text

        if state == QDoubleValidator.State.Intermediate:
            if text.startswith('0') and not text.startswith('0.'):
                return str(int(float(text)))

        if state == QDoubleValidator.State.Invalid:
            return text[:-1]

        # Ensure value is within range
        try:
            value = float(text)
            if value > self.max_value:
                return text[:-1]
        except ValueError:
            pass

        return text
