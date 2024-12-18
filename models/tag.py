from dataclasses import dataclass
from PyQt6.QtGui import QColor
from db import database
from typing import List
import logging

@dataclass
class Tag:
    text: str
    background: QColor
    foreground: QColor

    def is_valid(self) -> bool:
        return len(self.text) <= 16

class TagManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self._tags = None

        if database.is_connected():
           tags = database.get_tags()

           self._tags = { tag['key']: Tag(
                text=tag['content'],
                background=QColor(tag['background']),
                foreground=QColor(tag['foreground'])
            ) for tag in tags }
        else:
            self.logger.warning('Database is disconnected, tags were not initialized')

    def all(self) -> List[Tag]:
        """
        Returns all tags in the database
        """

        return list(self._tags.values())
    
    def get_tag(self, key: str) -> None:
        """
        Gets a tag with the specified key, if none can be found None is returned
        """

        return self._tags.get(key)