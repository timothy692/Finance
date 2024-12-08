from dataclasses import dataclass
from PyQt6.QtGui import QColor
import logging
from typing import List

@dataclass
class Tag:
    text: str
    background_color: QColor
    text_color: QColor

    def is_valid(self) -> bool:
        return len(self.text) <= 16

class TagManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self._tags = List[Tag]
    
    def add_tag(self, tag: Tag) -> bool:
        if tag.is_valid():
            self._tags.append(tag)

        return tag.is_valid()

    def add_tags(self, tags: List[Tag]) -> None:
        valids = [tag for tag in tags if tag.is_valid()]

        self._tags.extend(valids)
        if len(valids) != len(tags):
            self.logger.warning(f'{len(tags)-len(valids)} tags were invalid and not added!')

    def tags(self) -> List[Tag]:
        return self._tags 