from models.transaction import Transaction
from datetime import datetime

class FinanceService:
    def __init__(self):

        self._transactions = []

    def load(self, transactions: list[Transaction]) -> None:
        self._transactions = transactions

    def total_spending(self, month: int, year: int) -> float:
        """
        Calculates the total spending for the specified month and year
        """
        
        total = 0.0

        for t in self._transactions:
            date = t.convert_datetime()
            if t.amount > 0:
                continue
            
            if date.year == year and date.month == month:

                total -= t.amount

        return total
    
    def difference(self, x: float, y: float) -> int:
        """
        Calculates the signed percentage difference between x and y (rounded)\n
        A positive value indicates x > y, and a negative value indicates x < y
        """

        return round(100 * ((x - y) / ((x + y) / 2)))