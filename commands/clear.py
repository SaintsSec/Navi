#! /bin/python3

from mods import mods
import os

command = "/clear"
use = "Clears the screen"

def run():
    mods.clearScreen()
    os.system("cls" if os.name == 'nt' else 'clear')
    print(mods.art)
