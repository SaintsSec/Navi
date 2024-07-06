#!/bin/python3
command = "exit"
use = "Exit Navi"
aliases = ['quit', 'exit', 'goodbye']


def run(navi_instance, arguments=None):
    navi_instance.print_message(f"Thank you for stopping by! {navi_instance.get_user()}")
    exit(0)
