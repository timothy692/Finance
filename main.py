from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt as qt
import logging
import os
from app import App
from db import Database

def initLogger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )

os.environ["QT_QPA_PLATFORM"]           = "wayland" 
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_SCALE_FACTOR"]           = "0.6" 


if __name__ == '__main__':
    initLogger()
    
    # db = Database()
    
    # db.add_transaction(100.0, 'Description', 1000.0, None)

    # Init app
    app = App('Expense Tracker')
    app.run()