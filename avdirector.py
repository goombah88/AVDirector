#!/usr/bin/env python

import random
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path

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
)


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

        self.selectedBalls = []
        self.refreshBalls()

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
        #     chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

        # Separate module for GUI?
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(100, self.screen_height - 800, 400, 200)

        self.lblCurrentRoundTitle = QLabel("Current Round: ")

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
        self.btnNext.setDisabled(True)

        lblQuestions = QLabel("Questions for this round")
        self.lbxQuestions = QListWidget()

        self.currentRoundTitle = QLabel("Current Round: ")

        # Small display for host
        vboxSmallDisplay = QVBoxLayout()
        self.small_display = QLabel()
        self.small_display.setFixedSize(175, 175)
        self.small_display.setAlignment(Qt.AlignCenter)
        self.set_small_display(self.logo)
        vboxSmallDisplay.addWidget(self.small_display)
        self.small_display.setVisible(False)

        ###
        # Master HBox for all content
        vboxMaster = QVBoxLayout()
        ###

        # vboxRoundControls = QVBoxLayout()

        # Now add everything into the display
        hboxRoundControlButtons = QHBoxLayout()
        vboxButtons = QVBoxLayout()
        vboxButtons.addWidget(self.btnStartRound)
        vboxButtons.addWidget(self.btnEndRound)
        hboxRoundControlButtons.addLayout(vboxButtons)
        hboxRoundControlButtons.addWidget(self.btnNext)
        hboxRoundControlButtons.addLayout(vboxSmallDisplay)

        vboxMaster.addWidget(self.currentRoundTitle)
        vboxMaster.addLayout(hboxRoundControlButtons)
        vboxMaster.addWidget(lblQuestions)
        vboxMaster.addWidget(self.lbxQuestions)

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
        pixmap = QPixmap(self.pleaseStandBy).scaled(
            800, 800, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        self.dialog.load_image(pixmap)
        self.set_small_display(pixmap)
        self.dialogExists = True
        self.refreshBalls()
        self.btnNext.setEnabled(False)
        self.btnStartRound.setDisabled(False)
        self.presentWinningBalls()

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

    def refreshBalls(self):
        self.ball_dir = Path("balls/")
        self.ball_list = [
            f for f in listdir(self.ball_dir) if isfile(join(self.ball_dir, f))
        ]
        self.index_list = [*range(0, len(self.ball_list) - 1, 1)]

    def loadNextBall(self):
        new_ball = self.getNextBall()
        new_ball_path = "balls/" + new_ball
        pixmap = QPixmap(new_ball_path)
        self.dialog.load_image(pixmap)
        pixmap = QPixmap(new_ball_path).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)

    def getNextBall(self):
        self.activeRound = True
        while len(self.index_list) > 1:
            self.index_list = [*range(0, len(self.ball_list) - 1, 1)]
            chosen_index = random.choice(self.index_list)
            # print("Chosen Index:", chosen_index)
            chosen_ball = self.ball_list.pop(chosen_index)
            self.addToSelectedBallsList(chosen_ball)
            print("Chosen Ball:", chosen_ball)
            return chosen_ball

    def addToSelectedBallsList(self, new_ball):
        self.lbxQuestions.insertItem(0, str(new_ball).replace(".png", ""))

    def set_small_display(self, image_file):
        pixmap = QPixmap(image_file).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
