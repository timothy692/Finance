from PyQt6.QtGui import QDoubleValidator

class DoubleValidator:
    def __init__(self, currency: str, bottom: float = 0.01, top: float = 999999.99, decimals: int = 2):
        self.bottom = bottom
        self.top = top
        self.decimals = decimals
        self.currency_symbol = currency
        self.validator = QDoubleValidator(self.bottom, self.top, self.decimals)

    def validate(self, text: str) -> str:
        """
        Validates the given text and formats it as a double with a currency symbol.
        """
        
        # Remove currency symbol and unwanted characters
        if text.startswith(self.currency_symbol):
            text = text[1:].strip()

        text = text.replace('e', '').replace(',', '')

        state, _, _ = self.validator.validate(text, 0)

        if state == QDoubleValidator.State.Invalid:
            # If invalid, remove the last character
            text = text[:-1]
        elif state == QDoubleValidator.State.Intermediate:
            try:
                # Convert to float to check if it's valid
                value = float(text)
                if value >= self.top:
                    text = text[:-1]
                elif text.startswith('0') and not text.startswith('0.'):
                    text = str(int(value)) # Remove leading zeros
            except ValueError:
                pass

        return f"{self.currency_symbol} {text}" if text else ""
