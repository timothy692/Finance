import logging

from PyQt6.QtCore import QObject, pyqtSignal


class Repository(QObject):
    on_update = pyqtSignal(list)

    def __init__(self, db):
        super().__init__()

        self.logger = logging.getLogger(self.__class__.__name__)
        self._db = db
        self._conn = db.connection()

    def execute_query(self, query: str, params: any = None) -> list[tuple]:
        """
        Executes a query and returns the results, for read-only operations
        """
        if not self._db.is_connected(): 
            self.logger.error('Database is not connected, did not execute query')
            return []

        cursor = None

        try:
            cursor = self._conn.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()

            return results
        except Exception as e:
            self.logger.error(f'Could not execute query: {e}')

            return []
        finally:
            if cursor:
                cursor.close()

    def execute_commit(self, query: str, params: any = None) -> bool:
        """
        Executes a commit query, for write operations
        """
        
        if not self._db.is_connected():
            self.logger.error('Database is not connected, did not execute commit')
            return False

        cursor = None
        success = False

        try:
            cursor = self._conn.cursor()
            cursor.execute(query, params or ())
            self._conn.commit()

            success = True
        except Exception as e:
            self.logger.error(f'Could not execute commit: {e}')
            self._conn.rollback()  # Ensure invalid data is not committed to the database
        finally:
            if cursor:
                cursor.close()

        return success

    def execute_commit_many(self, query: str, params: list[tuple]) -> bool:
        """
        Executes a commit query in bulk, for write operations
        """
        if not self._db.is_connected():
            self.logger.error('Database is not connected, did not execute query')
            return False

        cursor = None
        success = False

        try:
            cursor = self._conn.cursor()
            cursor.executemany(query, params)
            self._conn.commit()

            success = True
        except Exception as e:
            self.logger.error(f'Could not execute commit many: {e}')
            self._conn.rollback()
        finally:
            if cursor:
                cursor.close()

        return success
