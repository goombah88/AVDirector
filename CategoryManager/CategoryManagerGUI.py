import random
import sys
from jproperties import Properties
import re

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    # QComboBox,
    QFileDialog,
    QDialog,
)

MAIN_WINDOW_HEIGHT = 500
MAIN_WINDOW_WIDTH = 700


class CategoryManager(QWidget):
    def __init__(self):
        super().__init__()

        # Set some defaults
        self.title = "Category Manager - Party Play Indy"
        self.logo = "ppi_logo.jpg"
        self.pleaseStandBy = "happiness.jpg"
        self.dialogExists = False
        self.lstQuestions = []
        self.lstAnswers = []

        # Separate module for GUI?
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(550, 350, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        vboxMain = QVBoxLayout()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CategoryManager()
    window.show()
    sys.exit(app.exec())
