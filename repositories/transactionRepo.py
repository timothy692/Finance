
from .repository import Repository


class TransactionRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def put_transaction(self, date: str, description: str, amount: float, balance: float, categories: list[str]|str, account: str) -> bool:
        """
        Inserts a single transaction to the database
        """
        
        return self.execute_commit('INSERT INTO transactions (date,description,amount,balance,category,account)', 
                            (date,description,amount,balance,categories,account))

    def put_transactions_many(self, transactions: list[dict[str, any]]) -> None:
        """
        Inserts transactions in bulk to the database
        """

        return self.execute_commit_many('INSERT INTO transactions (date,description,amount,balance,category,account)',
                                        transactions)