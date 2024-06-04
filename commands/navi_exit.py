#!/bin/python3
# imports
import os
from time import sleep
from navi_shell import get_ai_name, get_user, tr

command = "exit"
use = "Exit Navi"
aliases = ['quit', 'exit', 'goodbye']


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run():
    tr(f"{get_ai_name()} Thank you for stopping by! {get_user()}")
    exit(0)
