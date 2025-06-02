from abc import ABC, abstractmethod

class DataModel(ABC):
    @abstractmethod
    def to_tuple(self) -> tuple:
        """
        Converts the data model to a tuple\n
        Must be implemented by subclasses
        """

        pass