#! /bin/python3

from mods import mods

command = "/clear"
use = "Clears the screen"

def run():
    mods.clearScreen()
    print(mods.art)
