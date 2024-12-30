from PyQt6.QtGui import QColor

from models.tag import Tag

from .repository import Repository


class TagRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def fetch_tags(self, key: str=None) -> list[Tag] | Tag | None:
        '''
        If key is specified, a single tag is fetched from the database with the corresponding key\n
        If no key is specified, all tags from the database is fetched
        '''

        # Fetch a single tag from the db with the specified key
        if key:
            result = self.execute_query('SELECT key,content,background,foreground FROM tags WHERE key = ?', 
                               (key,))
            
            if len(result) == 0:
                return None
            
            row = result[0] # Grab the first result
            return Tag(
                    key=row[0],
                    text=row[1],
                    background=QColor(row[2]),
                    foreground=QColor(row[3])
                )

        # Fetch all tags from the db

        result = self.execute_query('SELECT key,content,background,foreground FROM tags')
        if len(result) == 0:
            return None

        return [
                Tag(
                    key=row[0],
                    text=row[1],
                    background=QColor(row[2]),
                    foreground=QColor(row[3])
                )

            for row in result
        ]