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
    QLineEdit,
    QPlainTextEdit,
)

MAIN_WINDOW_HEIGHT = 500
MAIN_WINDOW_WIDTH = 700
CATEGORY_CONFIG_FILE_EXT = ".ppc"


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

        # MASTER VBOX
        vboxMaster = QVBoxLayout()

        # QUESTION 1
        hboxQ1 = QHBoxLayout()
        lblQ1 = QLabel("Question 1:")
        self.txtQ1 = QPlainTextEdit(self)
        self.txtQ1.setLineWidth(400)
        self.txtQ1.setFixedHeight(100)
        hboxQ1.addWidget(lblQ1)
        hboxQ1.addWidget(self.txtQ1)
        hboxA1 = QHBoxLayout()
        lblA1 = QLabel("Answer 1:")
        self.txtA1 = QLineEdit()
        hboxA1.addWidget(lblA1)
        hboxA1.addWidget(self.txtA1)
        vboxMaster.addLayout(hboxQ1)
        vboxMaster.addLayout(hboxA1)

        # QUESTION 2
        hboxQ2 = QHBoxLayout()
        lblQ2 = QLabel("Question 2:")
        self.txtQ2 = QPlainTextEdit(self)
        self.txtQ2.setLineWidth(400)
        self.txtQ2.setFixedHeight(100)
        hboxQ2.addWidget(lblQ2)
        hboxQ2.addWidget(self.txtQ2)
        hboxA2 = QHBoxLayout()
        lblA2 = QLabel("Answer 2:")
        self.txtA2 = QLineEdit()
        hboxA2.addWidget(lblA2)
        hboxA2.addWidget(self.txtA2)
        vboxMaster.addLayout(hboxQ2)
        vboxMaster.addLayout(hboxA2)

        # QUESTION 3
        hboxQ3 = QHBoxLayout()
        lblQ3 = QLabel("Question 3:")
        self.txtQ3 = QPlainTextEdit(self)
        self.txtQ3.setLineWidth(400)
        self.txtQ3.setFixedHeight(100)
        hboxQ3.addWidget(lblQ3)
        hboxQ3.addWidget(self.txtQ3)
        hboxA3 = QHBoxLayout()
        lblA3 = QLabel("Answer 3:")
        self.txtA3 = QLineEdit()
        hboxA3.addWidget(lblA3)
        hboxA3.addWidget(self.txtA3)
        vboxMaster.addLayout(hboxQ3)
        vboxMaster.addLayout(hboxA3)

        # QUESTION 4
        hboxQ4 = QHBoxLayout()
        lblQ4 = QLabel("Question 4:")
        self.txtQ4 = QPlainTextEdit(self)
        self.txtQ4.setLineWidth(400)
        self.txtQ4.setFixedHeight(100)
        hboxQ4.addWidget(lblQ4)
        hboxQ4.addWidget(self.txtQ4)
        hboxA4 = QHBoxLayout()
        lblA4 = QLabel("Answer 4:")
        self.txtA4 = QLineEdit()
        hboxA4.addWidget(lblA4)
        hboxA4.addWidget(self.txtA4)
        vboxMaster.addLayout(hboxQ4)
        vboxMaster.addLayout(hboxA4)

        # BUTTON FOR TESTING FEATURES
        hboxTest = QHBoxLayout()
        btnTest = QPushButton("Test")
        btnTest.clicked.connect(self.saveConfigToFile)
        hboxTest.addWidget(btnTest)
        vboxMaster.addLayout(hboxTest)

        self.setLayout(vboxMaster)

    def saveToFile(self):
        print(self.txtQ3.toPlainText())

    def readConfigFromFile(self):
        pass

    def saveConfigToFile(self):
        fileName = "questions/abc"
        self.activeCategoryConfig = fileName + CATEGORY_CONFIG_FILE_EXT

        """
        # Read in the properties file
        questionsDict = {}
        configs = Properties()
        with open(self.activeCategoryConfig, "rb") as qFile:
            configs.load(qFile)
        items_view = configs.items()
        for item in items_view:
            questionsDict[item[0]] = item[1].data
            print(f"adding: {item[1].data}")
        # print(f"CONTENTS OF DICT: {questionsDict}")
        """
        configs = Properties()
        # if not configs["question3"]:
        print("no question 2. adding.")
        configs["question2"] = self.txtQ2.toPlainText()
        with open(self.activeCategoryConfig, "wb") as f:
            configs.store(f, encoding="utf-8")
        # print(f'Full name: {configs.get("name").data}')
        # print(f'Question 1: {configs.get("question1").data}')
        # print(f'Answer 1: {configs.get("answer1").data}')
        """
        index = 0
        while index < 5:
            for question in questionsDict:
                # print(f'index: {index}')
                _question = questionsDict.get(f"question{index}")
                _idx = f"{index+1}. "
                print(f"q is: {_question}")
                print(f"i is: {_idx}")
                self.listboxQuestions.insertItem(index, f"{_idx}{_question}")
                self.listboxAnswers.insertItem(
                    index, questionsDict.get(f"answer{index}")
                )
                index += 1

        # self.lbxQuestions.insertItem(0, configs.get("question1").data)

        # Set full category name
        self.lblCurrentRoundCategory.setText(configs.get("name").data)

        # _venues = list(configs.get("venues").data)
        # print(f'VENUES: {_venues}')
        # print(f'VENUES type: {type(_venues)}')

        c = configs.get("status").data + "," + "yo"
        if "yo" not in c:
            print("not found. adding it")
            print(f"NEW STATUS: {c}")
            configs["status"] = c
        else:
            print("found it. ignoring")

        with open(self.activeCategoryConfig, "wb") as f:
            configs.store(f)

        _status = configs.get("status").data
        print(f"STATUS: {_status}")
        print(f"STATUS TYPE: {type(_status)}")
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CategoryManager()
    window.show()
    sys.exit(app.exec())
