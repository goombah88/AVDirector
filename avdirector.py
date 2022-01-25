#!/usr/bin/env python

import random
import sys

# from os import listdir
# from os.path import isfile, join
# from pathlib import Path
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
)

# QUESTION_DIR = Path("questions/")


class Dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AVDirector - Party Play Indy")
        self.setStyleSheet("background-color: #00ffc4")
        self.logo = "ppi_logo.jpg"

        self.lblCategory = QLabel("Party Play Indy")
        self.lblCategory.resize(100, 100)
        # self.lblCategory.setSizePolicy(
        # QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.lblCategory.setAlignment(Qt.AlignCenter)
        # self.lblCategory.setFont(QFont('Comic Sans', 40))
        self.lblCategory.setStyleSheet(
            "background-color: #00ffc4; font: 40pt Times"
        )

        self.lblQuestion = QLabel()
        self.lblQuestion.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.lblQuestion.setAlignment(Qt.AlignCenter)
        self.lblQuestion.setFont(QFont("Comic Sans", 60))
        self.lblQuestion.setWordWrap(True)
        self.lblQuestion.setStyleSheet("background-color: white")
        pixmap = QPixmap(self.logo)
        self.lblQuestion.setPixmap(pixmap)

        # Pack it all in
        layout = QVBoxLayout(self)
        layout.addWidget(self.lblCategory)
        layout.addWidget(self.lblQuestion)

    def load_image(self, image):
        self.lblQuestion.setPixmap(image)

    def show_logo(self):
        self.lblQuestion.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(self.logo)
        self.setCategory("Party Play Indy")
        self.lblQuestion.setPixmap(pixmap)

    def setCategory(self, text):
        self.lblCategory.setText(text)

    def setQuestion(self, text):
        self.lblQuestion.setStyleSheet("background-color: #00ffc4")
        self.lblQuestion.setText(text)

    def showAllQuestions(self, text):
        self.lblQuestion.setAlignment(Qt.AlignVCenter)
        self.lblQuestion.setStyleSheet(
            "background-color: #00ffc4; font: 60pt Times"
        )
        self.lblQuestion.setText(text)


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set some defaults
        self.title = "AVDirector - Party Play Indy"
        self.logo = "ppi_logo.jpg"
        self.pleaseStandBy = "happiness.jpg"
        self.dialogExists = False
        self.activeRound = False
        self.lineCount = 0
        self.lstQuestions = []
        self.lstAnswers = []
        self.timerRoundOver = QTimer()

        self.selectedBalls = []

        # self.app = QApplication.instance()
        # self.screens_available = self.app.screens()
        # print("screens:", self.screens_available)
        # if self.screens_available == 0:
        #     self.selected_screen = 0
        # else:
        #     self.selected_screen = 1

        # self.screen = self.screens_available[self.selected_screen]
        # self.screen_width = self.screen.size().width()
        # self.screen_height = self.screen.size().height()
        # # Good default screen height for modern screens
        # self.screen_height = 1920

        # Get path to chrome
        # if platform.system() == "Linux":
        #     # Linux
        #     import termios
        #     chrome_path = '/usr/bin/google-chrome'
        # else:
        #     # Windows
        #     chrome_path =
        # 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

        # Separate module for GUI?
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(550, 350, 650, 450)

        self.lblCurrentRoundTitle = QLabel("Current Round: ")
        self.lblCurrentRoundTitle.setAlignment(Qt.AlignLeft)
        self.currentRoundTitle = QLabel()
        self.currentRoundTitle.setAlignment(Qt.AlignLeft)

        # StartRound Button
        self.btnStartRound = QPushButton("Start Round")
        self.btnStartRound.setFixedSize(250, 75)
        self.btnStartRound.clicked.connect(self.startNewRound)
        self.btnStartRound.setIcon(QIcon("start_icon.png"))
        self.btnStartRound.setIconSize(QSize(50, 50))

        # ShowLogo Button
        self.btnShowLogo = QPushButton()
        self.btnShowLogo.setFixedSize(100, 100)
        self.btnShowLogo.clicked.connect(self.showLogoInDialog)
        self.btnShowLogo.setIcon(QIcon("ppi_logo.jpg"))
        self.btnShowLogo.setIconSize(QSize(100, 100))

        # Next Button
        self.btnNext = QPushButton()
        self.btnNext.setFixedSize(175, 175)
        self.btnNext.clicked.connect(self.loadNextBall)
        self.btnNext.setIcon(QIcon("next_button.png"))
        self.btnNext.setIconSize(QSize(100, 100))
        self.btnNext.setDisabled(True)

        lblQuestions = QLabel("Questions for this round")
        self.listboxQuestions = QListWidget()
        self.listboxQuestions.clicked.connect(self.questionSelected)
        self.lblAnswers = QLabel("Answers for this round")
        self.listboxAnswers = QListWidget()
        self.lblAnswers.setVisible(False)
        self.listboxAnswers.setVisible(False)

        # Small display for host
        vboxSmallDisplay = QVBoxLayout()
        self.small_display = QLabel()
        self.small_display.setFixedSize(175, 175)
        self.small_display.setAlignment(Qt.AlignCenter)
        self.set_small_display(self.logo)
        vboxSmallDisplay.addWidget(self.small_display)
        self.small_display.setVisible(False)

        # self.comboCategories = QComboBox(self)
        # self.comboCategories.addItem("Select a Category")
        # self.comboCategories.activated[str].connect(self.onComboChanged)
        # self.lstQuestions = [
        #     f.replace(".ppc", "")
        #     for f in listdir(QUESTION_DIR)
        #     if isfile(join(QUESTION_DIR, f))
        # ]
        # print(f'Found categories: {self.lstQuestions}')
        # self.comboCategories\
        # .addItems(sorted(self.lstQuestions, key=str.lower))

        # Load file
        self.btnLoadFile = QPushButton("Load File")
        self.btnLoadFile.clicked.connect(self.loadFile)
        self.btnLoadFile.setDisabled(False)

        ###
        # PACK ALL THE THINGS!
        ###
        # Master HBox for all content
        vboxMaster = QVBoxLayout()
        ###

        hboxCurrentCategory = QHBoxLayout()
        hboxCurrentCategory.addWidget(self.lblCurrentRoundTitle)
        hboxCurrentCategory.addWidget(self.currentRoundTitle)

        # Now add everything into the display
        hboxRoundControlButtons = QHBoxLayout()
        vboxButtons = QVBoxLayout()
        # vboxButtons.addWidget(self.btnStartRound)
        # vboxButtons.addWidget(self.btnEndRound)
        # hboxRoundControlButtons.addWidget(self.comboCategories)
        hboxRoundControlButtons.addLayout(vboxButtons)
        hboxRoundControlButtons.addWidget(self.btnNext)
        hboxRoundControlButtons.addWidget(self.btnShowLogo)
        hboxRoundControlButtons.addLayout(vboxSmallDisplay)

        vboxMaster.addWidget(self.btnLoadFile)
        vboxMaster.addLayout(hboxCurrentCategory)
        vboxMaster.addWidget(self.currentRoundTitle)
        vboxMaster.addLayout(hboxRoundControlButtons)

        hboxQandA = QHBoxLayout()
        vboxQuestions = QVBoxLayout()
        vboxQuestions.addWidget(lblQuestions)
        vboxQuestions.addWidget(self.listboxQuestions)
        hboxQandA.addLayout(vboxQuestions)
        vboxAnswers = QVBoxLayout()
        vboxAnswers.addWidget(self.lblAnswers)
        vboxAnswers.addWidget(self.listboxAnswers)
        hboxQandA.addLayout(vboxAnswers)

        vboxMaster.addLayout(hboxQandA)

        self.setLayout(vboxMaster)

    def closeEvent(self, event):
        if self.activeRound:
            reply = QMessageBox.question(
                self,
                "Window Close",
                "Round in Progress. Sure ya wanna quit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            # print("reply:", reply)
            if reply == QMessageBox.Yes:
                event.accept()
                app.quit()
                # self.dialog.destroy()
            else:
                event.ignore()
        else:
            event.accept()
            app.quit()

    def startNewRound(self):
        self.activeRound = True
        self.btnStartRound.setDisabled(True)
        self.small_display.setVisible(True)
        self.btnNext.setEnabled(True)
        self.listboxQuestions.clear()
        if not self.dialogExists:
            self.dialog = Dialog()
            self.dialog.setGeometry(50, 50, 300, 300)
            self.dialog.show()
            self.btnNext.setDisabled(False)
            # self.dialogExists = True

    def showLogoInDialog(self):
        self.activeRound = False
        if not self.dialogExists:
            self.dialog = Dialog()
            self.dialog.setGeometry(50, 50, 300, 300)
            self.dialog.show()
        self.dialog.show_logo()
        self.dialogExists = True
        # self.set_small_display(pixmap)
        # self.presentWinningBalls()

    def loadNextBall(self):
        print("NEXT PRESSED")
        self.analyzeLine(self.lineCount)

        """new_ball = self.getNextBall()
        new_ball_path = "balls/" + new_ball
        pixmap = QPixmap(new_ball_path)
        self.dialog.load_image(pixmap)
        pixmap = QPixmap(new_ball_path).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)"""

    def getNextQuestion(self):
        self.activeRound = True
        while len(self.index_list) > 1:
            self.index_list = [*range(0, len(self.lstQuestions) - 1, 1)]
            chosen_index = random.choice(self.index_list)
            # print("Chosen Index:", chosen_index)
            chosen_ball = self.lstQuestions.pop(chosen_index)
            self.addQuestionToList(chosen_ball)
            print("Chosen Ball:", chosen_ball)
            return chosen_ball

    def addQuestionToList(self, question):
        self.listboxQuestions.insertItem(0, str(question).replace(".ppq", ""))

    def set_small_display(self, image_file):
        pixmap = QPixmap(image_file).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)

    def onComboChanged(self, text):
        print(f"{text} activated")
        self.activeCategory = text
        # self.activeFile = f"{QUESTION_DIR}/{self.activeCategory}.ppq"
        print(f"cat: {self.activeCategory}, file: {self.activeFile}")
        self.readInQuestions(self.activeFile)

    def readInQuestions(self, questionFile):
        self.listboxQuestions.clear()
        self.listboxAnswers.clear()
        # Read in the properties file
        questionsDict = {}
        configs = Properties()
        with open(questionFile, "rb") as qFile:
            configs.load(qFile)
        items_view = configs.items()
        for item in items_view:
            questionsDict[item[0]] = item[1].data
            print(f"adding: {item[1].data}")
        print(f"CONTENTS OF DICT: {questionsDict}")

        # print(f'Full name: {configs.get("name").data}')
        # print(f'Question 1: {configs.get("question1").data}')
        # print(f'Answer 1: {configs.get("answer1").data}')
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
        self.currentRoundTitle.setText(configs.get("name").data)

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

        with open(questionFile, "wb") as f:
            configs.store(f)

        _status = configs.get("status").data
        print(f"STATUS: {_status}")
        print(f"STATUS TYPE: {type(_status)}")

    def questionSelected(self, model):
        self.listboxAnswers.setCurrentRow(model.row())

    def loadFile(self, inputFile):
        inputFile = self.getFileName()
        with open(inputFile, encoding="utf-8-sig") as fp:
            # self.contents = fp.readlines()
            self.contents = [line for line in fp.readlines() if line.strip()]
        # print(f"ALL CONTENTS:{self.contents}")
        # print("CALLING RUN")
        self.btnNext.setDisabled(False)
        if not self.dialogExists:
            self.dialog = Dialog()
            self.dialog.setGeometry(50, 50, 300, 300)
            self.dialog.show()
            self.dialogExists = True

        self.analyzeLine(0)

    def getFileName(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            # "All Files (*);;Python Files (*.py)",
            "Party Play Indy Config Files (*.ppc)",
            options=options,
        )
        if self.fileName:
            print(f"file: {self.fileName}")
            return self.fileName
            # self.run(self.fileName)
            # Read text file to list

    def analyzeLine(self, lineCount):
        self.lineCount = lineCount
        # if lineCount == -1:
        #     # This means we're starting fresh
        #     self.lstQuestions = []
        #     self.lstAnswers = []

        # Read in text file
        # Keep track of where we left off in the file with lineCount
        # with open(inputFile) as self.fp:
        #     while self.getProceed():
        # lines = self.fp.readlines()
        # Skip to the line we left off on
        # for i in range(self.lineCount):
        #     fp, next(i)
        line = self.contents[self.lineCount]
        # if self.lineCount == 0:
        #     print("First run")
        #     line = self.contents[self.lineCount]
        # else:
        #     line = self.contents[self.lineCount + 1]
        # for line in lines:
        # if line[0].isalpha():
        print(f"LINE:{line}")
        print(f"CURRENT LINE COUNT:{self.lineCount}")

        # END CHECK
        if re.search("^END$", line):
            # print(f'END:{line}')
            self.dialog.show_logo()
            self.dialog.setCategory("Name That TUNE!")
            self.btnNext.setDisabled(True)

        # CATEGORY CHECK
        if re.search("^[A-Z][a-z]", line):
            # print(f'CATEGORY:{line}')
            self.updateCategory(line.strip())

        # BLANK LINE CHECK
        # if line == "\n":
        #     print("BLANK LINE")
        #     self.analyzeLine(self.lineCount)

        # QUESTION CHECK
        if line[0].isdigit():
            # QUESTION, Display it
            # print(f'QUESTION:{line}')
            self.updateQuestion(line.strip())

        # ANSWER CHECK
        if re.search("^\t[a-zA-Z]*", line):
            # print(f'ANSWER:{line}')
            self.updateAnswers(line.strip())

        print("incrementing counter")
        self.lineCount += 1

    def updateCategory(self, category):
        print(f"CATEGORY:{category}")
        self.reset()
        self.currentRoundTitle.setText(category.strip())
        self.dialog.setCategory(category)
        # self.dialog.setQuestion(category)

    def updateQuestion(self, question):
        self.lstQuestions.append(question)
        self.listboxQuestions.clear()
        self.listboxQuestions.addItems(self.lstQuestions)
        print(f"QUESTION:{question}")
        # self.analyzeLine(self.lineCount)
        self.dialog.setQuestion(question)

    def updateAnswers(self, answer):
        print(f"ANSWER:{answer}, {len(self.lstAnswers)}")
        self.lstAnswers.append(answer)
        if len(self.lstAnswers) == 5:
            self.listboxAnswers.addItems(self.lstAnswers)
            self.lblAnswers.setVisible(True)
            self.listboxAnswers.setVisible(True)

            # Display all 5 questions for people
            questions = ""
            for q in self.lstQuestions:
                questions += q + "\n"
            self.dialog.showAllQuestions(questions)
        # self.analyzeLine(self.lineCount)

    def reset(self):
        self.lblAnswers.setVisible(False)
        self.listboxAnswers.setVisible(False)
        self.lstQuestions.clear()
        self.lstAnswers.clear()
        self.listboxQuestions.clear()
        self.listboxAnswers.clear()
        self.dialog.show_logo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
