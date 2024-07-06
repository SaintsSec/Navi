#!/bin/python3

command = "clear"
use = "Clear the screen"
aliases = ['cls']


def run(navi_instance,arguments=None):
    navi_instance.clear_terminal()
    navi_instance.print_message(f"How can I help you, {navi_instance.get_user()}?")
