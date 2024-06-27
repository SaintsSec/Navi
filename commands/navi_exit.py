#!/bin/python3
from navi_shell import get_user, print_message

command = "exit"
use = "Exit Navi"
aliases = ['quit', 'exit', 'goodbye']


def run(arguments=None):
    print_message(f"Thank you for stopping by! {get_user()}")
    exit(0)
