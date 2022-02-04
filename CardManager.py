import sys

# from jproperties import Properties
import configparser
from os.path import exists, basename
from dateutil.rrule import rrule, WEEKLY, MO

# from models.Category import Category


# from PyQt5.QtCore import QSize, Qt, QTimer
# from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    # QListWidget,
    # QMessageBox,
    QPushButton,
    # QSizePolicy,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QFileDialog,
    # QDialog,
    QLineEdit,
    QPlainTextEdit,
)

MAIN_WINDOW_HEIGHT = 500
MAIN_WINDOW_WIDTH = 700
CATEGORY_FILE_EXT = ".ppc"
QUESTION_BOX_HEIGHT = 75
QUESTION_BOX_WIDTH = 400
CATEGORIES_FOLDER = "categories/"


class CardManager(QWidget):
    def __init__(self):
        super().__init__()

        # Set some defaults
        self.title = "Category Manager - Party Play Indy"
        self.logo = "ppi_logo.jpg"
        self.pleaseStandBy = "happiness.jpg"
        self.dialogExists = False
        self.lstQuestions = []
        self.lstAnswers = []
        self.listOfNext12Mondays = []
        self.activeFileName = ""

        # List the next 12 Mondays
        for date in rrule(WEEKLY, byweekday=MO, count=12):
            self.listOfNext12Mondays.append(
                f"{date.month}-{date.day}-{date.year}"
            )
        self.selectedMonday = self.listOfNext12Mondays[0]
        # print(self.listOfNext12Mondays)
        print(self.selectedMonday)

        # Separate module for GUI?
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(550, 350, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)

        # MASTER VBOX
        vboxMaster = QVBoxLayout()

        hboxButtons = QHBoxLayout()

        # LABEL
        self.lblInfo = QLabel(
            "<b>Load a Card to edit or start creating a new Card.</b>"
        )
        vboxMaster.addWidget(self.lblInfo)

        # LOAD BUTTON
        btnLoad = QPushButton("Load")
        btnLoad.clicked.connect(self.loadFile)
        hboxButtons.addWidget(btnLoad)

        # SAVE BUTTON
        btnSave = QPushButton("Save")
        btnSave.clicked.connect(self.saveConfigToFile)
        hboxButtons.addWidget(btnSave)

        # NEW BUTTON
        # btnNew = QPushButton("New")
        # btnNew.clicked.connect(self.createNewCategoryFile)
        # hboxButtons.addWidget(btnNew)

        vboxMaster.addLayout(hboxButtons)

        hboxCategoryName = QHBoxLayout()
        lblCategoryName = QLabel("Full Name for this Category: ")
        self.txtCategoryName = QLineEdit()
        hboxCategoryName.addWidget(lblCategoryName)
        hboxCategoryName.addWidget(self.txtCategoryName)
        vboxMaster.addLayout(hboxCategoryName)

        hboxMondays = QHBoxLayout()
        lblMondays = QLabel("This is for the week of (appended to filename): ")
        self.comboMondays = QComboBox(self)
        # self.comboMondays.addItem("Select a Week")
        self.comboMondays.activated[str].connect(self.onComboChanged)
        # print(f'Found categories: {self.lstQuestions}')
        self.comboMondays.addItems(self.listOfNext12Mondays)
        # .addItems(sorted(self.lstQuestions, key=str.lower))
        hboxMondays.addWidget(lblMondays)
        hboxMondays.addWidget(self.comboMondays)
        vboxMaster.addLayout(hboxMondays)

        # QUESTION 1
        hboxQ1 = QHBoxLayout()
        lblQ1 = QLabel("Question 1:")
        self.txtQ1 = QPlainTextEdit(self)
        self.txtQ1.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ1.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ1.addWidget(lblQ1)
        hboxQ1.addWidget(self.txtQ1)
        hboxA1 = QHBoxLayout()
        lblA1 = QLabel("                Answer 1:")
        self.txtA1 = QLineEdit()
        hboxA1.addWidget(lblA1)
        hboxA1.addWidget(self.txtA1)
        vboxMaster.addLayout(hboxQ1)
        vboxMaster.addLayout(hboxA1)

        # QUESTION 2
        hboxQ2 = QHBoxLayout()
        lblQ2 = QLabel("Question 2:")
        self.txtQ2 = QPlainTextEdit(self)
        self.txtQ2.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ2.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ2.addWidget(lblQ2)
        hboxQ2.addWidget(self.txtQ2)
        hboxA2 = QHBoxLayout()
        lblA2 = QLabel("                Answer 2:")
        self.txtA2 = QLineEdit()
        hboxA2.addWidget(lblA2)
        hboxA2.addWidget(self.txtA2)
        vboxMaster.addLayout(hboxQ2)
        vboxMaster.addLayout(hboxA2)

        # QUESTION 3
        hboxQ3 = QHBoxLayout()
        lblQ3 = QLabel("Question 3:")
        self.txtQ3 = QPlainTextEdit(self)
        self.txtQ3.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ3.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ3.addWidget(lblQ3)
        hboxQ3.addWidget(self.txtQ3)
        hboxA3 = QHBoxLayout()
        lblA3 = QLabel("                Answer 3:")
        self.txtA3 = QLineEdit()
        hboxA3.addWidget(lblA3)
        hboxA3.addWidget(self.txtA3)
        vboxMaster.addLayout(hboxQ3)
        vboxMaster.addLayout(hboxA3)

        # QUESTION 4
        hboxQ4 = QHBoxLayout()
        lblQ4 = QLabel("Question 4:")
        self.txtQ4 = QPlainTextEdit(self)
        self.txtQ4.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ4.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ4.addWidget(lblQ4)
        hboxQ4.addWidget(self.txtQ4)
        hboxA4 = QHBoxLayout()
        lblA4 = QLabel("                Answer 4:")
        self.txtA4 = QLineEdit()
        hboxA4.addWidget(lblA4)
        hboxA4.addWidget(self.txtA4)
        vboxMaster.addLayout(hboxQ4)
        vboxMaster.addLayout(hboxA4)

        # QUESTION 5
        hboxQ5 = QHBoxLayout()
        lblQ5 = QLabel("Question 5:")
        self.txtQ5 = QPlainTextEdit(self)
        self.txtQ5.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ5.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ5.addWidget(lblQ5)
        hboxQ5.addWidget(self.txtQ5)
        hboxA5 = QHBoxLayout()
        lblA5 = QLabel("                Answer 5:")
        self.txtA5 = QLineEdit()
        hboxA5.addWidget(lblA5)
        hboxA5.addWidget(self.txtA5)
        vboxMaster.addLayout(hboxQ5)
        vboxMaster.addLayout(hboxA5)

        self.setLayout(vboxMaster)

    def loadFile(self):
        # fileName = "categories/abc.ppc"

        # for item in range(1, 6):
        #     if configs.get("question1"):
        #         print(f"doing {item}")
        #         self.txtQ1.setPlainText(configs.get("question1").data)
        #         self.txtA1.setText(configs.get("answer1").data)
        # else:
        #     print("skipping 1")

        configs = configparser.ConfigParser()
        self.activeFileName = self.getLoadFileName()
        configs.read(self.activeFileName)

        self.activeCategory = configs["META"]["name"]
        self.txtCategoryName.setText(self.activeCategory)
        # self.activeCategory = splitext(basename(self.activeFileName))[0]
        # print(f"active category is {self.activeCategory}")

        # print(f'basename:{basename(self.fileName)},\
        #     with strip:{basename(self.fileName)\
        # .strip(CATEGORY_CONFIG_FILE_EXT)}')
        self.updateInfoLabel(self.activeCategory)
        print(f"active file is {self.activeFileName}")
        # Populate fields from chosen file
        # if questionsDict.get("question1"):
        #     print("doing Q1")

        # Hard-coded for now
        # TODO: Make question/answer count variable
        q1 = configs["CONTENT"]["question1"]
        a1 = configs["CONTENT"]["answer1"]
        q2 = configs["CONTENT"]["question2"]
        a2 = configs["CONTENT"]["answer2"]
        q3 = configs["CONTENT"]["question3"]
        a3 = configs["CONTENT"]["answer3"]
        q4 = configs["CONTENT"]["question4"]
        a4 = configs["CONTENT"]["answer4"]
        q5 = configs["CONTENT"]["question5"]
        a5 = configs["CONTENT"]["answer5"]
        self.txtQ1.setPlainText(q1)
        self.txtA1.setText(a1)
        self.txtQ2.setPlainText(q2)
        self.txtA2.setText(a2)
        self.txtQ3.setPlainText(q3)
        self.txtA3.setText(a3)
        self.txtQ4.setPlainText(q4)
        self.txtA4.setText(a4)
        self.txtQ5.setPlainText(q5)
        self.txtA5.setText(a5)

    def getLoadFileName(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "categories/",
            # "All Files (*);;Python Files (*.py)",
            "Party Play Indy Category Files (*.ppc)",
            options=options,
        )
        if fileName:
            print(f"opening file: {fileName}")
            return fileName

    def saveConfigToFile(self):
        print("saving to file.")
        fileName = self.getSaveFileName()
        configs = configparser.ConfigParser()
        configs.read(fileName)

        if self.txtCategoryName.text():
            catName = self.txtCategoryName.text()
        else:
            catName = basename(fileName).replace(CATEGORY_FILE_EXT, "")

        configs.set("META", "name", catName)
        configs.set("META", "venues_used", self.txtQ1.toPlainText())
        configs.set("CONTENT", "question1", self.txtQ1.toPlainText())
        configs.set("CONTENT", "answer1", self.txtA1.text())
        configs.set("CONTENT", "question2", self.txtQ2.toPlainText())
        configs.set("CONTENT", "answer2", self.txtA2.text())
        configs.set("CONTENT", "question3", self.txtQ3.toPlainText())
        configs.set("CONTENT", "answer3", self.txtA3.text())
        configs.set("CONTENT", "question4", self.txtQ4.toPlainText())
        configs.set("CONTENT", "answer4", self.txtA4.text())
        configs.set("CONTENT", "question5", self.txtQ5.toPlainText())
        configs.set("CONTENT", "answer5", self.txtA5.text())
        # configs.write(self.activeCategoryConfig)
        with open(fileName, "w") as f:
            configs.write(f)
        # configs.read(self.activeCategoryConfig)
        # print(f'Full name: {configs.get("name").data}')
        # print(f'Question 1: {configs.get("question1").data}')
        # print(f'Answer 1: {configs.get("answer1").data}')

    def getSaveFileName(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "%s%s_%s"
            % (
                CATEGORIES_FOLDER,
                self.sanitize_filename(self.txtCategoryName.text()),
                self.selectedMonday,
            ),
            # "All Files (*);;Python Files (*.py)",
            "Party Play Indy Category Files (*.ppc)",
            options=options,
        )
        if fileName:
            fileName += CATEGORY_FILE_EXT
            print(f"got fileName: {fileName}")
            self.createNewCategoryFile(fileName)
            return fileName
        else:
            print(f"file does not exist. creating {fileName}")

    def createNewCategoryFile(self, fileName):
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getSaveFileName(
        #     self,
        #     "QFileDialog.getSaveFileName()",
        #     "%s%s" % (CATEGORIES_FOLDER, self.selectedMonday),
        #     "Party Play Indy Category Files (*.ppc)",
        #     options=options,
        # )
        # if fileName:
        #     fileName += CATEGORY_FILE_EXT
        #     print(fileName)

        configs = configparser.ConfigParser()

        # https://stackoverflow.com/questions/44907415/configparser-create-file-if-it-doesnt-exist
        if not exists(fileName):
            configs.add_section("META")
            configs.add_section("CONTENT")
            configs.write(open(fileName, "w"))
        # else:
        #     configs.read(fileName)

        with open(fileName, "w") as f:
            configs.write(f)

    def updateInfoLabel(self, text):
        self.lblInfo.setText(
            'You are editing <div style="font-family: Times; font-size: 30px;\
                font-style: bold; font-weight: bold;">'
            + text
            + "</div>"
        )

    def onComboChanged(self, text):
        self.selectedMonday = text
        print(f"{self.selectedMonday} selected")
        # self.activeFile = f"{QUESTION_DIR}/{self.activeCategory}.ppq"
        # print(f"cat: {self.activeCategory}, file: {self.activeFile}")

    def sanitize_filename(self, string):
        sanitized = "".join(x for x in string if x.isalnum())
        return sanitized


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardManager()
    window.show()
    sys.exit(app.exec())
