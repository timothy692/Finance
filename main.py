from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt as qt
import logging
import os
from app import App

def initLogger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )

os.environ["QT_QPA_PLATFORM"]           = "wayland" 
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_SCALE_FACTOR"]           = "0.7" 
# os.environ["QT_FONT_DPI"]               = "96"


if __name__ == '__main__':
    initLogger()
        
    # db.add_transaction('09.08.2023 13:42', 'Test', 100.0, 100.0, ['Food'], 'Credit Card')

    # Init app
    app = App('Expense Tracker')
    app.run()