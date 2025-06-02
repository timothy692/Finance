from datetime import datetime

from models.transaction import Transaction
from repositories.transactionRepo import TransactionRepository
from db import database

class FinanceService:
    def __init__(self, transaction_repo: TransactionRepository):
        self._repo = transaction_repo

        self._transactions = transaction_repo.fetch_transactions()
        transaction_repo.update.connect(self._update_transactions)
    
    def _update_transactions(self, transactions: list[Transaction]) -> None:
        self._transactions.extend(transactions) 

    def calculate_total(self, month: int, year: int, income: bool) -> float:
        """
        Calculate total income or spending for the given month and year
        """

        total = 0.0

        for t in self._transactions:
            date = t.convert_datetime()
            if (income and t.amount < 0) or (not income and t.amount > 0):
                continue

            if date.year == year and date.month == month:
                total += t.amount if income else -t.amount

        return total
    
    def difference_for_ratio(self, x: float, y: float) -> float:
        """
        Calculates the percentage difference between x and y,
        scaled relative to the larger value\n
        A positive value indicates x > y, and a negative value indicates x < y
        """

        if x == y:
            return 0.0  # No difference

        # Determine the larger value for scaling
        larger = max(abs(x), abs(y))

        # Calculate the percentage difference
        diff = ((x - y) / larger) * 100

        return round(diff)