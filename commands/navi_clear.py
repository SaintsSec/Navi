#!/bin/python3
# imports
import os
from navi_shell import get_ai_name, get_user, tr

command = "clear"
use = "Clear the screen"
aliases = ['cls']


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run():
    clear_screen()
    tr(f"{get_ai_name()} How can I help you, {get_user()}?")
