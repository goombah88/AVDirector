import sys
from jproperties import Properties
import configparser


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
    # QComboBox,
    # QFileDialog,
    # QDialog,
    QLineEdit,
    QPlainTextEdit,
)

MAIN_WINDOW_HEIGHT = 500
MAIN_WINDOW_WIDTH = 700
CATEGORY_CONFIG_FILE_EXT = ".ppc"
QUESTION_BOX_HEIGHT = 75
QUESTION_BOX_WIDTH = 400


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

        hboxButtons = QHBoxLayout()

        # LOAD BUTTON
        btnLoad = QPushButton("Load")
        btnLoad.clicked.connect(self.loadFile)
        hboxButtons.addWidget(btnLoad)

        # BUTTON
        btnSave = QPushButton("Save")
        btnSave.clicked.connect(self.saveConfigToFile)
        hboxButtons.addWidget(btnSave)
        vboxMaster.addLayout(hboxButtons)

        # QUESTION 1
        hboxQ1 = QHBoxLayout()
        lblQ1 = QLabel("Question 1:")
        self.txtQ1 = QPlainTextEdit(self)
        self.txtQ1.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ1.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ1.addWidget(lblQ1)
        hboxQ1.addWidget(self.txtQ1)
        hboxA1 = QHBoxLayout()
        lblA1 = QLabel("Answer 1:")
        self.txtA1 = QLineEdit()
        self.txtA1
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
        self.txtQ3.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ3.setFixedHeight(QUESTION_BOX_HEIGHT)
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
        self.txtQ4.setLineWidth(QUESTION_BOX_WIDTH)
        self.txtQ4.setFixedHeight(QUESTION_BOX_HEIGHT)
        hboxQ4.addWidget(lblQ4)
        hboxQ4.addWidget(self.txtQ4)
        hboxA4 = QHBoxLayout()
        lblA4 = QLabel("Answer 4:")
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
        lblA5 = QLabel("Answer 5:")
        self.txtA5 = QLineEdit()
        hboxA5.addWidget(lblA5)
        hboxA5.addWidget(self.txtA5)
        vboxMaster.addLayout(hboxQ5)
        vboxMaster.addLayout(hboxA5)

        self.setLayout(vboxMaster)

    def loadFile(self):
        # TESTING
        fileName = "questions/abc.ppc"
        ###
        # Read in the properties file
        # dictContent = {}
        # configs = Properties()
        # with open(fileName, "rb") as qFile:
        #     configs.load(qFile)
        # items_view = configs.items()
        # for item in items_view:
        #     dictContent[item[0]] = item[1].data
        #     print(f"adding: {item[1].data}")
        # print(f"CONTENTS OF DICT: {dictContent}")

        # for item in range(1, 6):
        #     if configs.get("question1"):
        #         print(f"doing {item}")
        #         self.txtQ1.setPlainText(configs.get("question1").data)
        #         self.txtA1.setText(configs.get("answer1").data)
        # else:
        #     print("skipping 1")

        configs = configparser.SafeConfigParser()
        configs.read(fileName)
        # Populate fields from chosen file
        # if questionsDict.get("question1"):
        #     print("doing Q1")
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

        # if dictContent.get("question1") else self.txtQ1.setPlainText(
        #     "default value"
        # )
        # self.txtA1.setText(configs.get("answer1").data) if dictContent.get(
        #     "answer1"
        # ) else self.txtA1.setText("default answer")
        # self.txtQ2.setPlainText(
        #     configs.get("question2").data
        # ) if dictContent.get("question2") else self.txtQ2.setPlainText(
        #     "default value"
        # )
        # self.txtA2.setText(configs.get("answer2").data) if dictContent.get(
        #     "answer2"
        # ) else self.txtA2.setText("default answer")
        # self.txtQ3.setPlainText(
        #     configs.get("question3").data
        # ) if dictContent.get("question3") else self.txtQ3.setPlainText(
        #     "default value"
        # )
        # self.txtA3.setText(configs.get("answer3").data) if dictContent.get(
        #     "answer3"
        # ) else self.txtA3.setText("default answer")
        # self.txtQ4.setPlainText(
        #     configs.get("question4").data
        # ) if dictContent.get("question4") else self.txtQ4.setPlainText(
        #     "default value"
        # )
        # self.txtA4.setText(configs.get("answer4").data) if dictContent.get(
        #     "answer4"
        # ) else self.txtA4.setText("default answer")
        # self.txtQ5.setPlainText(
        #     configs.get("question5").data
        # ) if dictContent.get("question5") else self.txtQ5.setPlainText(
        #     "default value"
        # )
        # self.txtA5.setText(configs.get("answer5").data) if dictContent.get(
        #     "answer5"
        # ) else self.txtA5.setText("default answer")

        """
        self.txtQ1.setPlainText(configs.get("question1").data)\
            if questionsDict.get("question1")\
            else self.txtQ1.setPlainText("default value")

        self.txtA1.setText(configs.get("answer1").data)\
            if questionsDict.get("answer1")\
            else self.txtA1.setText("default answer")
        # else:
        #     print("skipping 1")
        self.txtQ2.setPlainText(configs.get("question2").data)
        self.txtA2.setText(configs.get("answer2").data)
        self.txtQ3.setPlainText(configs.get("question3").data)
        self.txtA3.setText(configs.get("answer3").data)
        self.txtQ4.setPlainText(configs.get("question4").data)
        self.txtA4.setText(configs.get("answer4").data)
        self.txtQ5.setPlainText(configs.get("question5").data)
        self.txtA5.setText(configs.get("answer5").data)
        """

    def saveConfigToFile(self):
        fileName = "questions/abc"
        self.activeCategoryConfig = fileName + CATEGORY_CONFIG_FILE_EXT

        # cat = Category("why?", "beCuz")
        # print(f"BEFORE Q1:{cat.q1}, A1:{cat.a1}")
        # Category.q1 = "questionONE"
        # Category.a1 = "answerONE"
        # print(f"AFTER Q1:{cat.q1}, A1:{cat.a1}")

        # configs = Properties()
        # if not configs["question3"]:
        print("writing to file.")
        # configs["question1"] = self.txtQ1.toPlainText()
        # configs["answer1"] = self.txtA1.text()
        # configs["question2"] = self.txtQ2.toPlainText()
        # configs["answer2"] = self.txtA2.text()

        # configs["question4"] = self.txtQ4.toPlainText()
        # configs["answer4"] = self.txtA4.text()
        # configs["question5"] = self.txtQ5.toPlainText()
        # configs["answer5"] = self.txtA5.text()

        # with open(self.activeCategoryConfig, "wb") as f:
        #     configs.store(f, encoding="utf-8")
        # print(
        #     f'AFTER Q1:{configs.get("question1").data}, \
        #     A1:{configs.get("answer1").data}'
        # )

        configs = configparser.SafeConfigParser()
        configs.read(self.activeCategoryConfig)
        x = configs["CONTENT"]["question3"]
        print(f"q3:{x}")
        self.txtQ3.setPlainText(x)
        # configs.set("CONTENT", "question3", self.txtQ3.toPlainText())
        # configs.set("CONTENT", "answer3", self.txtA3.text())
        # configs.write(self.activeCategoryConfig)
        with open(self.activeCategoryConfig, "w") as f:
            configs.write(f)
        configs.read(self.activeCategoryConfig)
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
