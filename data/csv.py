import csv
from typing import Dict, List

from PyQt6.QtWidgets import QFileDialog


class CSV:
    def __init__(self):
        self.BANK_HEADER_MAPPINGS = {
            'Swedbank': {
                'Radnummer': None,
                'Bokföringsdag': None,
                'Transaktionsdag': 'date',
                'Valutadag': None,
                'Referens': None,
                'Beskrivning': 'description',
                'Belopp': 'amount',
                'Bokfört saldo': 'balance',
            }
        }

    def validate_headers(self, bank: str, headers: List[str]) -> Dict[str,str]:
        """
        Validates the list of headers, leaving out unnecessary headers\n
        Returns a dictionary containing the raw and translated header
        """

        valids = {}
        mapping = self.BANK_HEADER_MAPPINGS.get(bank)
        
        for header in headers:
            if header in list(mapping.keys()) and mapping[header]:
                valids[header] = mapping[header]

        return valids
    
    def parse_csv(self, bank: str, content: List[List[str]]) -> List[Dict[str,any]]:
        """
        Returns a list of dictionaries containing the transaction data 
        """
        
        data = [{}]
        indexed_headers = {}
        start_idx = 0

        for n,row in enumerate(content):
            # Skip rows that do not contain a transaction
            if any(s is None or s == '' for s in row):
                continue

            # Populating headers dictionary with indices and translated header
            headers = self.validate_headers(bank=bank, headers=row)
            for idx,col in enumerate(row):
                if col in list(headers.keys()):
                    indexed_headers[idx] = headers[col]

            start_idx = n+1
            break

        # Start parsing from the header to end of file
        for row in content[start_idx:]:
            row_data = {}

            for idx,header in indexed_headers.items():
                item = row[idx]

                # Convert number columns to floats
                if header in ['amount', 'balance']:
                    item = item.replace(',', '').strip()

                    row_data[header] = float(item)
                    continue

                row_data[header] = item

            data.append(row_data)

        return data

    def import_csv(self) -> List[Dict[str,any]] | None:
        """
        Opens a QFileDialog to import a CSV file\n
        Returns a list of dictionaries containing the transaction data, if accepted
        """

        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter('CSV Files (*.csv)')
        dialog.setViewMode(QFileDialog.ViewMode.List)

        if dialog.exec():
            file = dialog.selectedFiles()[0]
            
            with open(file, mode='r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)

                return self.parse_csv(bank='Swedbank', content=[line for line in reader])
            
        return None