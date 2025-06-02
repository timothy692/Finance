from abc import ABC, abstractmethod

from PyQt6.QtCore import pyqtSlot, pyqtSignal


class DynamicWidget:
    def __init__(self):
        pass

    @abstractmethod
    def update(self, values: dict) -> None:
        """
        Called on update, must be implemented
        """

        pass