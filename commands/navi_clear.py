#!/bin/python3
from navi_shell import get_ai_name, get_user, pre_run, tr

command = "clear"
use = "Clear the screen"
aliases = ['cls']


def run(arguments=None):
    pre_run()
    tr(f"{get_ai_name()} How can I help you, {get_user()}?")
