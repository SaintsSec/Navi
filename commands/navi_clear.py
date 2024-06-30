#!/bin/python3
from navi_shell import get_user, clear_terminal, print_message

command = "clear"
use = "Clear the screen"
aliases = ['cls']


def run(arguments=None):
    clear_terminal()
    print_message(f"How can I help you, {get_user()}?")
