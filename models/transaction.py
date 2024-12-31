import datetime
from dataclasses import dataclass

from .tag import Tag


@dataclass
class Transaction:
    identifier: int
    date: str
    description: str
    amount: float
    balance: float
    categories: list[Tag]
    account: str

    def convert_datetime(self, format='%d%m%y') -> datetime.date:
        stripped = self.date.replace('.', '').replace('-', '').replace('/', '')

        return datetime.datetime.strptime(stripped, format).date()