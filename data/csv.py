import csv

from PyQt6.QtWidgets import QFileDialog
from charset_normalizer import from_path

from models.transaction import Transaction


class CSV:
    def __init__(self):
        self.BANK_HEADER_MAPPINGS = {
            'Swedbank': {
                'Radnummer': None,
                'Bokföringsdag': None,
                'Valutadag': None,
                'Referens': None,
                'Transaktionsdag': 'date',
                'Beskrivning': 'description',
                'Belopp': 'amount',
                'Bokfört saldo': 'balance', 
                # category here
                'Produkt': 'account', 
            }
        }

        self._data = []

    def validate_headers(self, bank: str, headers: list[str]) -> dict[str,str]:
        """
        Validates the list of valid headers\n
        Returns a dictionary containing the index and translated header
        """

        valids = {}
        mapping = self.BANK_HEADER_MAPPINGS.get(bank)
        
        for idx,header in enumerate(headers):
            s = header.strip()

            if s in list(mapping.keys()) and mapping[s]:
                valids[mapping[s]] = idx

        return valids
    
    def parse_csv(self, bank: str, content: list[list[str]]) -> list[Transaction]:
        """
        Returns a list of dictionaries containing the transaction data 
        """
        
        data = []
        indexed_headers = {}
        start_idx = 0

        for n,row in enumerate(content):
            # Skip rows that do not contain a transaction
            if any(s is None or s == '' for s in row):
                continue

            indexed_headers = self.validate_headers(bank=bank, headers=row)

            start_idx = n+1
            break
        
        for row in content[start_idx:]:
            data_dict = {header: row[index] for header, index in indexed_headers.items()}
            
            data.append(Transaction(
                date=data_dict['date'],
                description=data_dict['description'],
                amount=data_dict['amount'],
                balance=data_dict['balance'],
                account=data_dict['account'],
                category=[],                            # TODO: tag algorithm
            ))

        return data
    
    def data(self) -> list[Transaction]:
        return self._data

    def import_csv(self) -> bool:
        """
        Opens a QFileDialog to import a CSV file\n
        Returns True if a file was successfully opened
        """

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('CSV Files (*.csv)')
        dialog.setViewMode(QFileDialog.ViewMode.List)

        if dialog.exec():
            file = dialog.selectedFiles()[0]

            encoding = from_path(file).best().encoding

            with open(file, mode='r', encoding=encoding) as f:
                reader = csv.reader(f)

                self._data = self.parse_csv(bank='Swedbank', content=[line for line in reader])
            return True
        else:
            return False