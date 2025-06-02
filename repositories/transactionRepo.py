
from models.transaction import Transaction

from .repository import Repository


class TransactionRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def fetch_transactions(self) -> list[Transaction]:
        """
        Fetch all transactions from the database
        """

        transactions = []

        result = self.execute_query('SELECT * FROM transactions')

        for row in result:
            # Convert category string back to a list
            category = str(row[6]).split(',')

            transactions.append(Transaction(
                identifier=row[0],

                date=row[1], description=row[2], 
                amount=row[3], balance=row[4], 
                account=row[5], category=category
            ))

        return transactions

    def put_transaction(self, transaction: Transaction) -> bool:
        """
        Inserts a single transaction to the database\n
        Emits a signal to on_update on success
        """
        
        success = self.execute_commit('INSERT INTO transactions (date,description,amount,balance,category,account) \
                                      VALUES (?,?,?,?,?,?)', 
                                    transaction.to_tuple())
        
        if success:
            self.update.emit([transaction])

        return success

    def put_transactions_many(self, transactions: list[Transaction]) -> None:
        """
        Inserts transactions in bulk to the database\n
        Emits a signal to on_update on success
        """

        success = self.execute_commit_many('INSERT INTO transactions (date,description,amount,balance,category,account) \
                                        VALUES (?,?,?,?,?,?)', [t.to_tuple() for t in transactions])
        
        if success:
            self.update.emit(transactions)

        return success