#!/bin/python3
from navi_shell import get_ai_name, get_user, tr

command = "exit"
use = "Exit Navi"
aliases = ['quit', 'exit', 'goodbye']


def run(arguments=None):
    tr(f"Thank you for stopping by! {get_user()}")
    exit(0)
