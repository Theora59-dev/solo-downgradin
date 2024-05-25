
#####################################################
###########   Bibliothèques externes  ###############
#####################################################

import pygame as pg
import os
import time
import subprocess
import sys

from colorama import Fore, Back

print(">>>>> Bibliothèques externes chargés")

#####################################################
###########   Bibliothèques internes  ###############
#####################################################

import settings

print(">>>>> Bibliothèques internes chargées")
#####################################################
#####################################################
#####################################################

print(">>>>> Lancement du jeu...")
pg.init()
pg.mixer.init()
pg.joystick.init()

joysticks = []

for i in range(pg.joystick.get_count()):
    joysticks.append(pg.joystick.Joystick(i))


for joystick in joysticks:
    joystick.init()



from ui.game import *
python_executable = sys.executable
script_to_run = "src/game/easter_egg/snake.py"
#subprocess.run([python_executable, script_to_run])
