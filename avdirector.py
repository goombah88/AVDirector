#!/usr/bin/env python

import random
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path
from jproperties import Properties
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    # QButtonGroup,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    # QRadioButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QFileDialog,
)

QUESTION_DIR = Path("questions/")


class Dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "AVDirector - Party Play Indy"
        self.logo = "ppi_logo.jpg"
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(self.logo)
        self.label.setPixmap(pixmap)
        lay = QVBoxLayout(self)
        lay.addWidget(self.label)

    def load_image(self, image):
        self.label.setPixmap(image)


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set some defaults
        self.title = "AVDirector - Party Play Indy"
        self.logo = "ppi_logo.jpg"
        self.pleaseStandBy = "happiness.jpg"
        self.dialogExists = False
        self.activeRound = False
        self.proceed = False

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
        self.currentRoundTitle = QLabel()

        # StartRound Button
        self.btnStartRound = QPushButton("Start Round")
        self.btnStartRound.setFixedSize(250, 75)
        self.btnStartRound.clicked.connect(self.startNewRound)
        self.btnStartRound.setIcon(QIcon("start_icon.png"))
        self.btnStartRound.setIconSize(QSize(50, 50))

        # EndRound Button
        self.btnEndRound = QPushButton("End Round")
        self.btnEndRound.setFixedSize(250, 75)
        self.btnEndRound.clicked.connect(self.endRound)
        self.btnEndRound.setDisabled(True)
        self.btnEndRound.setIcon(QIcon("end_icon.png"))
        self.btnEndRound.setIconSize(QSize(50, 50))

        # Next Button
        self.btnNext = QPushButton()
        self.btnNext.setFixedSize(175, 175)
        self.btnNext.clicked.connect(self.loadNextBall)
        self.btnNext.setIcon(QIcon("next_button.jpg"))
        self.btnNext.setIconSize(QSize(100, 100))
        self.btnNext.setDisabled(False)

        lblQuestions = QLabel("Questions for this round")
        self.lbxQuestions = QListWidget()
        self.lbxQuestions.clicked.connect(self.questionSelected)
        lblAnswers = QLabel("Answers for this round")
        self.lbxAnswers = QListWidget()

        # Small display for host
        vboxSmallDisplay = QVBoxLayout()
        self.small_display = QLabel()
        self.small_display.setFixedSize(175, 175)
        self.small_display.setAlignment(Qt.AlignCenter)
        self.set_small_display(self.logo)
        vboxSmallDisplay.addWidget(self.small_display)
        self.small_display.setVisible(False)

        self.comboCategories = QComboBox(self)
        self.comboCategories.addItem("Select a Category")
        self.comboCategories.activated[str].connect(self.onComboChanged)
        self.lstQuestions = [f.replace(".ppq", "") for f in listdir(QUESTION_DIR) if isfile(join(QUESTION_DIR, f))]
        # print(f'Found categories: {self.lstQuestions}')
        self.comboCategories.addItems(sorted(self.lstQuestions, key=str.lower))

        # Load file
        self.btnLoadFile = QPushButton("Load File")
        self.btnLoadFile.clicked.connect(self.getFileName)
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
        vboxButtons.addWidget(self.btnStartRound)
        vboxButtons.addWidget(self.btnEndRound)
        hboxRoundControlButtons.addWidget(self.comboCategories)
        hboxRoundControlButtons.addLayout(vboxButtons)
        hboxRoundControlButtons.addWidget(self.btnNext)
        hboxRoundControlButtons.addLayout(vboxSmallDisplay)

        vboxMaster.addWidget(self.btnLoadFile)
        vboxMaster.addLayout(hboxCurrentCategory)
        vboxMaster.addWidget(self.currentRoundTitle)
        vboxMaster.addLayout(hboxRoundControlButtons)

        hboxQandA = QHBoxLayout()
        vboxQuestions = QVBoxLayout()
        vboxQuestions.addWidget(lblQuestions)
        vboxQuestions.addWidget(self.lbxQuestions)
        hboxQandA.addLayout(vboxQuestions)
        vboxAnswers = QVBoxLayout()
        vboxAnswers.addWidget(lblAnswers)
        vboxAnswers.addWidget(self.lbxAnswers)
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
        self.lbxQuestions.clear()
        if not self.dialogExists:
            self.dialog = Dialog()
            self.dialog.setGeometry(50, 50, 300, 300)
            self.dialog.show()
            self.btnNext.setDisabled(False)
            self.btnEndRound.setDisabled(False)
            self.dialogExists = True

    def endRound(self):
        self.activeRound = False
        pixmap = QPixmap(self.pleaseStandBy).scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.dialog.load_image(pixmap)
        self.set_small_display(pixmap)
        self.dialogExists = True
        self.btnNext.setEnabled(False)
        self.btnStartRound.setDisabled(False)
        # self.presentWinningBalls()

    def presentWinningBalls(self):
        # Sort all selectedBalls by letter then number
        # to make it easier to check winners
        letters = ["b", "i", "n", "g", "o"]
        sorted_balls = []
        for letter in letters:
            """For each letter in B.I.N.G.O. sort the balls
            from each letter and add them to the listwidget"""
            temp_balls = []
            print("checking letter", letter)
            for ball in range(self.lbxQuestions.count()):
                if self.lbxQuestions.item(ball).text().startswith(letter):
                    print("adding", self.lbxQuestions.item(ball).text())
                    temp_balls.append(self.lbxQuestions.item(ball).text())
                    print("temp_balls:", temp_balls)
            if temp_balls:
                for ball in sorted(temp_balls):
                    sorted_balls.append(ball)
                sorted_balls.append("-----")

        print("sorted_balls:", sorted_balls)

        self.lbxQuestions.clear()
        for ball in sorted_balls:
            self.lbxQuestions.addItem(str(ball))

    def loadNextBall(self):
        print("NEXT PRESSED")
        self.run(self.fileName)

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
        self.lbxQuestions.insertItem(0, str(question).replace(".ppq", ""))

    def set_small_display(self, image_file):
        pixmap = QPixmap(image_file).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)

    def onComboChanged(self, text):
        print(f"{text} activated")
        self.activeCategory = text
        self.activeFile = f"{QUESTION_DIR}/{self.activeCategory}.ppq"
        print(f"cat: {self.activeCategory}, file: {self.activeFile}")
        self.readInQuestions(self.activeFile)

    def readInQuestions(self, questionFile):
        self.lbxQuestions.clear()
        self.lbxAnswers.clear()
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
                self.lbxQuestions.insertItem(index, f"{_idx}{_question}")
                self.lbxAnswers.insertItem(index, questionsDict.get(f"answer{index}"))
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
        self.lbxAnswers.setCurrentRow(model.row())

    def getFileName(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options
        )
        if self.fileName:
            print(f"file: {self.fileName}")
            self.lineCount = 1
            self.run(self.fileName)

    def run(self, inputFile):
        if self.lineCount == 1:
            # This means we're starting fresh
            self.lstQuestions = []
            self.lstAnswers = []

        # Read in text file
        # Keep track of where we left off in the file with lineCount
        with open(inputFile) as fp:
            lines = fp.readlines()
            # Skip to the line we left off on
            # for i in range(self.lineCount):
            #     fp, next(i)
            for line in lines:
                print(f'CHECKING LINE:{self.lineCount}')
                # if line[0].isalpha():

                # CATEGORY CHECK
                if re.search("^[A-Z][a-z]", line):
                    # print(f'CATEGORY:{line}')
                    self.updateCategory(line.strip())

                # BLANK LINE CHECK
                if line.isspace():
                    # print('BLANK LINE')
                    continue

                # QUESTION CHECK
                if line[0].isdigit():
                    # QUESTION, Display it
                    # print(f'QUESTION:{line}')
                    break
                    self.updateQuestion(line.strip())

                # ANSWER CHECK
                if re.search("^\\t+[A-Z]*", line):
                    # print(f'ANSWER:{line}')
                    self.addAnswerToList(line.strip())
                    break

                self.lineCount += 1

    def updateCategory(self, category):
        print(f"Updating Category to {category}")
        self.currentRoundTitle.setText(category)

    def updateQuestion(self, question):
        self.lstQuestions.append(question)
        self.lbxQuestions.clear()
        self.lbxQuestions.addItems(self.lstQuestions)
        print(f"Updating Question to {question}")
        self.run(self.fileName)

    def addAnswerToList(self, answer):
        self.lstAnswers.append(answer)
        if len(self.lstAnswers) == 5:
            self.lbxAnswers.addItems(self.lstAnswers)
        print(f"Adding answer {answer}")
    
    def wait():
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
