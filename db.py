import logging
import sqlite3 as sql
from datetime import datetime
from typing import Dict, List


class Database:
    def __init__(self, db_name='database.db'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._conn = None
        self._db_name = db_name

        self.try_connect(db_name)
        self._init_tables()

    def try_connect(self, filename: str) -> bool:
        try:
            self._conn = sql.connect(filename)
            self.logger.info(f'Successfully connected to database (\'{self._db_name}\')')
            return True
        except sql.Error as e:
            self.logger.error(f'Could not connect to database (\'{self._db_name}\'): {e}')
            return False

    def disconnect(self) -> None:
        self._conn.close()
        self.logger.info(f'Disconnected from database (\'{self._db_name}\')')

    def connection(self) -> None:
        return self._conn
    
    def is_connected(self) -> bool:
        try:
            self._conn.cursor()
            return True
        except Exception:
            return False
    
    def _create_tag_key(self, content: str) -> None:
        return content.lower().replace(' ', '-')

    def _init_tables(self) -> None:
        with self._conn:
            cursor = self._conn.cursor()

            statements = [
                '''
                CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL,
                        balance REAL NOT NULL,
                        category TEXT,
                        account TEXT NOT NULL );
                ''',

                '''
                CREATE TABLE IF NOT EXISTS tags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT NOT NULL,
                        content TEXT NOT NULL,
                        background TEXT NOT NULL,
                        foreground TEXT NOT NULL );
                '''
            ]

            for statement in statements:
                cursor.execute(statement)

            default_tags = [
                ("Basic", "#e0f7ff", "#1F509A"),
                ("Must have", "#FFE0E0", "#AF1740"),
                ("Income", "#E8F5E9", "#2E7D32"),
                ("Sport", "#F5E0FF", "#7B1FA2"),
                ("Health", "#E0F7FF", "#017B92"),
                ("Food", "#F5F5F5", "#545454"),
                ("Entertainment", "#FFF2E0", "#BF360C")
            ]

            cursor.executemany('''
                INSERT INTO tags (key,content,background,foreground) SELECT ?,?,?,?
                WHERE NOT EXISTS (
                    SELECT 1 FROM tags WHERE content = ?
                );
            ''', [(self._create_tag_key(tag[0]), tag[0], tag[1], tag[2], tag[0]) for tag in default_tags])
            
            self.logger.info('Initialized tables')
        
    def add_transaction(self, date: str, description: str, amount: float, balance: float, categories: List[str]|str, account: str) -> None:
        """
        Adds a single transaction into the database
        """
        
        with self._conn:
            cursor = self._conn.cursor()
            category = ' '.join(categories) if isinstance(categories, list) else categories

            cursor.execute('''
                INSERT INTO transactions (date,description,amount,balance,category,account) 
                           VALUES (?,?,?,?,?,?);
            ''', (date,description,amount,balance,category,account))
            
            self.logger.info(f'Inserted transaction id #{cursor.lastrowid}')

    def add_transactions(self, transactions: List[Dict[str, any]]) -> None:
        """
        Adds transactions in bulk into the database

        Args:
            A list of transaction dicts (date,description,amount,balance,category,account)
        """

        with self._conn:
            cursor = self._conn.cursor()
            
            # Prepare the data to be inserted into the database
            data = [
                (
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['balance'],
                    transaction['category'],
                    transaction['account']
                )

                for transaction in transactions
            ]

            cursor.executemany('''
                INSERT INTO transactions (date,description,amount,balance,category,account) 
                           VALUES (?,?,?,?,?,?);
                ''', data)
            
            self.logger.info(f'Inserted {cursor.rowcount} transactions')

    def get_tags(self, key: str=None) -> List[Dict[str,any]]|Dict[str,any]|None:
        '''
        Retrieves all tags from the database if key not specified

        Args:
            key: The key of the tag

        Returns:
            A list of dict or single dict containing each tag data (content,background,foreground)
        '''

        with self._conn:
            cursor = self._conn.cursor()
            if key:
                cursor.execute('SELECT key,content,background,foreground FROM tags WHERE key = ?', (key,))
                row = cursor.fetchone()

                if not row:
                    return None
                else:
                    return {
                        'key': row[0],
                        'content': row[1],
                        'background': row[2],
                        'foreground': row[3]
                    }
            
            # Retrieve all tags

            cursor.execute('SELECT key,content,background,foreground FROM tags')
            rows = cursor.fetchall()

            return [
                {
                    'key':row[0],
                    'content': row[1], 
                    'background': row[2], 
                    'foreground': row[3]
                }
                for row in rows
            ]
        

# Initialize a global instance of database
database = Database('database.db')