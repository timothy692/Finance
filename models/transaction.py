import datetime
from dataclasses import field, dataclass

from .tag import Tag
from .dataModel import DataModel


@dataclass
class Transaction(DataModel):
    identifier: int = 0 # The identifier corresponds to the unique id in the database
    date: str = ''
    description: str = ''
    amount: float = 0.0
    balance: float = 0.0
    account: str = ''
    category: list[Tag] = field(default_factory=list)

    def convert_datetime(self, _format='%Y%m%d') -> datetime.date:
        stripped = self.date.replace('.', '').replace('-', '').replace('/', '')

        return datetime.datetime.strptime(stripped, _format).date()
    
    def to_tuple(self) -> tuple:
        # Convert list of tags to concatenated  string
        category = ','.join([tag.text for tag in self.category])
        
        return (self.date, self.description, self.amount, self.balance, category, self.account)