#!/usr/bin/env python

import os, sys, time
from os import listdir, path
from os.path import isfile, join
import random
import webbrowser
import platform
from pathlib import Path

ball_dir = Path("balls/")

if platform.system() == "Linux":
    # Linux
    import termios
    chrome_path = '/usr/bin/google-chrome'
else:
    # Windows
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def getkey():
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

ball_list = [f for f in listdir(ball_dir) if isfile(join(ball_dir, f))]
index_list = [*range(0, len(ball_list) - 1, 1)]

#starting_length = len(ball_list)
#print("length:", length)
#starting_indexes = 75

#for index,file in enumerate(ball_list):
    #print(index, file)

# Open new window with logo to hold bingo tabs
webbrowser.get('chrome').open_new("")
time.sleep(3)
webbrowser.get('chrome').open("ppi_logo.jpg", new=0, autoraise=False)
input("Press Enter to continue")

while (len(index_list) > 1):
    index_list = [*range(0, len(ball_list) - 1, 1)]
    chosen_index = random.choice(index_list)
    #print("Chosen Index:", chosen_index)
    chosen_ball = ball_list.pop(chosen_index)
    print("Chosen Ball:", chosen_ball)
    #x = input("Press Any Key For Next Ball")
    #to_open = str(ball_dir / chosen_ball)
    #print("to_open:%s/%s" % (chrome_path, to_open))
    webbrowser.get('chrome').open(str(ball_dir / chosen_ball))
    input("Press Any Key For Next Ball (or q to quit)")
    if platform.system() == "Linux":
        a = getkey()
        print("got key", a)
        if a == "q":
            sys.exit(0)
        else:
            continue

print("ALL DONE")
