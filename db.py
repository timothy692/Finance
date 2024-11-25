import sqlite3 as sql
import logging

class Database:
    def __init__(self, db_name='database.db'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._conn = None
        self._db_name = db_name

        self.try_connect(db_name)
        self.create_tables()

    def try_connect(self, filename: str) -> bool:
        try:
            self._conn = sql.connect(filename)
            self.logger.info(f'Successfully connected to db (\'{self._db_name}\')')
            return True
        except sql.Error as e:
            self.logger.error(f'Could not connect to db (\'{self._db_name}\'): {e}')
            return False

    def disconnect(self) -> None:
        self._conn.close()
        self.logger.info(f'Disconnected from db (\'{self._db_name}\')')

    def create_tables(self) -> None:
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount REAL NOT NULL,
                            category TEXT,
                            description TEXT NOT NULL,
                            balance REAL NOT NULL);''')
            
            self.logger.info('Initialized tables')
        
    def add_transaction(self, amount: float, description: str, balance: float, category: str=None) -> None:
        with self._conn:
            cursor = self._conn.cursor()
            cursor.execute('''INSERT INTO transactions (amount, category, description, balance)
                            VALUES (?, ?, ?, ?)''', (amount, category, description, balance))
            
            self.logger.info(f'Inserted transaction: ({amount}, \'{category}\', \'{description}\', {balance})')