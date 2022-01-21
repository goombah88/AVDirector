#!/usr/bin/env python

import time
import platform
import random
import sys
from os import listdir
from os.path import isfile, join
from pathlib import Path
#from typing import Deque

#from playsound import playsound
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QHBoxLayout, QLabel, QListWidget,
                             QMessageBox, QPushButton, QRadioButton,
                             QSizePolicy, QVBoxLayout, QWidget)

TIMER_DURATION = 1
AUDIO_SLEEP_TIME_SECONDS = 2

class Dialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "AVDirector - Party Play Indy"
        self.logo = 'ppi_logo.jpg'
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
        self.logo = 'ppi_logo.jpg'
        self.pleaseStandBy = 'happiness.jpg'
        self.dialogExists = False
        self.activeRound = False
        self.mode = 'manual'
        self.audioMode = 'off'
        self.secondsLeftInTimer = TIMER_DURATION
        
        self.selectedBalls = []
        self.refreshBalls()
        self.app = QApplication.instance()
        self.screens_available = self.app.screens()
        #print("screens:", self.screens_available)
        if self.screens_available == 0:
            self.selected_screen = 0
        else:
            self.selected_screen = 1

        self.screen = self.screens_available[self.selected_screen]
        self.screen_width = self.screen.size().width()
        self.screen_height = self.screen.size().height()
        
        if platform.system() == "Linux":
            # Linux
            import termios
            chrome_path = '/usr/bin/google-chrome'
        else:
            # Windows
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
       
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, self.screen_height - 310, 400, 200)

        # StartRound Button
        self.btnStartRound = QPushButton("Start Round")
        self.btnStartRound.setFixedSize(250, 75)
        self.btnStartRound.clicked.connect(self.startNewRound)
        self.btnStartRound.setIcon(QIcon('start_icon.png'))
        self.btnStartRound.setIconSize(QSize(50,50))

        # EndRound Button
        self.btnEndRound = QPushButton("End Round")
        self.btnEndRound.setFixedSize(250, 75)
        self.btnEndRound.clicked.connect(self.endRound)
        self.btnEndRound.setDisabled(True)
        self.btnEndRound.setIcon(QIcon('end_icon.png'))
        self.btnEndRound.setIconSize(QSize(50,50))

        # Next Button
        self.btnNext = QPushButton()
        self.btnNext.setFixedSize(175, 175)
        self.btnNext.clicked.connect(self.loadNextBall)
        self.btnNext.setIcon(QIcon('next_button.jpg'))
        self.btnNext.setIconSize(QSize(100,100))
        self.btnNext.setDisabled(True)

        self.previousBallListbox = QListWidget()

        hboxOptions = QHBoxLayout()
        self.radioBtnGroupMode = QButtonGroup()
        self.radioBtnGroupAudio = QButtonGroup()

        # Auto/Manual Toggle
        self.radioManual = QRadioButton("Manual")
        self.radioManual.setChecked(True)
        self.radioManual.mode = "manual"
        self.radioManual.toggled.connect(self.modeSelected)

        self.radioAuto = QRadioButton("Auto")
        self.radioAuto.setChecked(False)
        self.radioAuto.mode = "auto"
        self.radioAuto.toggled.connect(self.modeSelected)

        self.radioBtnGroupMode.addButton(self.radioManual)
        self.radioBtnGroupMode.addButton(self.radioAuto)
       
        hboxRadioButtons = QHBoxLayout()
        hboxRadioButtons.addWidget(self.radioManual)
        hboxRadioButtons.addWidget(self.radioAuto)

        # Audio ON/OFF
        hboxAudioRadioButtons = QHBoxLayout()

        self.radioAudioOn = QRadioButton("On")
        self.radioAudioOn.setChecked(False)
        self.radioAudioOn.audiomode = "on"
        self.radioAudioOn.toggled.connect(self.audioModeSelected)
        hboxAudioRadioButtons.addWidget(self.radioAudioOn)

        self.radioAudioOff = QRadioButton("Off")
        self.radioAudioOff.setChecked(True)
        self.radioAudioOff.audiomode = "off"
        self.radioAudioOff.toggled.connect(self.audioModeSelected)
        hboxAudioRadioButtons.addWidget(self.radioAudioOff)

        self.radioBtnGroupAudio.addButton(self.radioAudioOn)
        self.radioBtnGroupAudio.addButton(self.radioAudioOff)

        # Timer
        hboxTimer = QHBoxLayout()
        self.lblTimeLeft = QLabel()
        self.lblTimeLeft.setText(str(self.secondsLeftInTimer))
        label = QLabel("sec remaining")
        hboxTimer.addWidget(self.lblTimeLeft)
        hboxTimer.addWidget(label)

        hboxOptions.addLayout(hboxRadioButtons)
        hboxOptions.addLayout(hboxAudioRadioButtons)
        hboxOptions.addLayout(hboxTimer)

        # Small display for host
        vboxSmallDisplay = QVBoxLayout()
        self.small_display = QLabel()
        self.small_display.setFixedSize(175, 175)
        #self.small_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.small_display.setAlignment(Qt.AlignCenter)
        self.set_small_display(self.logo)
        vboxSmallDisplay.addWidget(self.small_display)
        self.small_display.setVisible(False)

        ###
        vboxMaster = QVBoxLayout()
        ###

        hboxMain = QHBoxLayout()
        hboxMain.addWidget(self.previousBallListbox)
        vboxButtons = QVBoxLayout()
        vboxButtons.addWidget(self.btnStartRound)
        vboxButtons.addWidget(self.btnEndRound)
        hboxMain.addLayout(vboxButtons)
        hboxMain.addWidget(self.btnNext)
        hboxMain.addLayout(vboxSmallDisplay)

        vboxMaster.addLayout(hboxMain)
        vboxMaster.addLayout(hboxOptions)

        self.setLayout(vboxMaster)

    def closeEvent(self, event):
        if self.activeRound:
            reply = QMessageBox.question(self, "Window Close", 'Round in Progress. Really Close?', 
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            #print("reply:", reply)
            if reply == QMessageBox.Yes:
                event.accept()
                app.quit()
                #self.dialog.destroy()
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
        self.previousBallListbox.clear()
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
        self.timer_stop()
        self.refreshBalls()
        self.btnNext.setEnabled(False)
        self.btnStartRound.setDisabled(False)
        self.presentWinningBalls()

    def presentWinningBalls(self):
        # Sort all selectedBalls by letter then number to make it easier to check winners
        letters = ['b', 'i', 'n', 'g', 'o']
        sorted_balls = []
        for letter in letters:
            '''For each letter in B.I.N.G.O. sort the balls from each letter and add them to the listwidget'''
            temp_balls = []
            print("checking letter", letter)
            for ball in range(self.previousBallListbox.count()):
                if self.previousBallListbox.item(ball).text().startswith(letter):
                    print("adding", self.previousBallListbox.item(ball).text())
                    temp_balls.append(self.previousBallListbox.item(ball).text())  
                    print("temp_balls:", temp_balls)
            if temp_balls:
                for ball in sorted(temp_balls):
                    sorted_balls.append(ball)
                sorted_balls.append('-----')

        print("sorted_balls:", sorted_balls)

        self.previousBallListbox.clear()
        for ball in sorted_balls:
            self.previousBallListbox.addItem(str(ball))

    def refreshBalls(self):
        self.ball_dir = Path("balls/")
        self.ball_list = [f for f in listdir(self.ball_dir) if isfile(join(self.ball_dir, f))]
        self.index_list = [*range(0, len(self.ball_list) - 1, 1)]

    def loadNextBall(self):
        new_ball = self.getNextBall()
        new_ball_path = "balls/" + new_ball
        pixmap = QPixmap(new_ball_path)
        self.dialog.load_image(pixmap)
        pixmap = QPixmap(new_ball_path).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)
        self.timer_start()
        new_sound = "sounds/" + new_ball.replace(".png", ".mp3")
        """ try:
            playsound(new_sound)
            time.sleep(AUDIO_SLEEP_TIME_SECONDS)
            playsound(new_sound)
        except:
            pass """

    def getNextBall(self):
        self.activeRound = True
        while (len(self.index_list) > 1):
            self.index_list = [*range(0, len(self.ball_list) - 1, 1)]
            chosen_index = random.choice(self.index_list)
            #print("Chosen Index:", chosen_index)
            chosen_ball = self.ball_list.pop(chosen_index)
            self.addToSelectedBallsList(chosen_ball)
            print("Chosen Ball:", chosen_ball)
            return chosen_ball

    def addToSelectedBallsList(self, new_ball):
        self.previousBallListbox.insertItem(0, str(new_ball).replace(".png", ""))

    def modeSelected(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.mode = radioButton.mode
            print("Mode is %s" % (self.mode))

    def audioModeSelected(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.audioMode = radioButton.audiomode
            print("Audio Mode is %s" % (self.audioMode))

    def timer_start(self):
        self.secondsLeftInTimer = TIMER_DURATION
        self.timerCountdown = QtCore.QTimer(self)
        self.timerCountdown.timeout.connect(self.timer_timeout)
        self.timerCountdown.start(1000)
        self.btnNext.setEnabled(False)

        self.update_gui()

    def timer_stop(self):
        self.timerCountdown.stop()
        self.lblTimeLeft.setText(str(TIMER_DURATION))

    def timer_timeout(self):
        if self.secondsLeftInTimer > 0:            
            self.secondsLeftInTimer -= 1
        else:
            self.timerCountdown.stop()
            self.btnNext.setEnabled(True)
            if self.mode == "auto":
                self.loadNextBall()
                #self.timerLeft = TIMER_DURATION
        self.update_gui()

    def update_gui(self):
        self.lblTimeLeft.setText(str(self.secondsLeftInTimer))

    def set_small_display(self, image_file):
        pixmap = QPixmap(image_file).scaledToWidth(175).scaledToHeight(175)
        self.small_display.setPixmap(pixmap)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
