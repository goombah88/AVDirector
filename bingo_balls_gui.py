#!/usr/bin/env python

import os, sys, time
from os import listdir, path
from os.path import isfile, join
import random
import webbrowser
import platform
import termios
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class BingoBallsMaster(QWidget):
   
    def __init__(self):
        super().__init__()
        self.title = 'Bingo Time!'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.ball_dir = Path("balls/")
        self.new_method()
        
        if platform.system() == "Linux":
            # Linux
            import termios
            chrome_path = '/usr/bin/google-chrome'
        else:
            # Windows
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        self.initUI()
        self.run()

    def new_method(self):
        self.ball_list = [f for f in listdir(self.ball_dir) if isfile(join(self.ball_dir, f))]
        self.index_list = [*range(0, len(self.ball_list) - 1, 1)]

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def getkey(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0
        termios.tcsetattr(fd, termios.TCSANOW, new)
        c = None
        try:
            c = os.read(fd, 1)
            #flush_to_stdout(c)
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        if c == b'\x7f': # Backspace/delete is hit
            return "delete"
        return c.decode("utf-8")


    #starting_length = len(ball_list)
    #print("length:", length)
    #starting_indexes = 75

    #for index,file in enumerate(ball_list):
        #print(index, file)

    def run(self):
        # Open new window with logo to hold bingo tabs
        self.webbrowser.get('chrome').open_new("")
        time.sleep(3)
        self.webbrowser.get('chrome').open("ppi_logo.jpg", new=0, autoraise=False)
        input("Press Enter to continue")

        while (len(self.index_list) > 1):
            self.index_list = [*range(0, len(self.ball_list) - 1, 1)]
            chosen_index = random.choice(self.index_list)
            #print("Chosen Index:", chosen_index)
            chosen_ball = self.ball_list.pop(chosen_index)
            print("Chosen Ball:", chosen_ball)
            #x = input("Press Any Key For Next Ball")
            #to_open = str(ball_dir / chosen_ball)
            #print("to_open:%s/%s" % (chrome_path, to_open))
            self.webbrowser.get('chrome').open(str(self.ball_dir / chosen_ball))
            input("Press Any Key For Next Ball (or q to quit)")
            if platform.system() == "Linux":
                a = self.getkey()
                print("got key", a)
                if a == "q":
                    sys.exit(0)
                else:
                    continue

        print("ALL DONE")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BingoBallsMaster()
    window.show()
    #app.exec()
    sys.exit(app.exec_())