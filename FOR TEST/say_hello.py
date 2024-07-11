#!/bin/python3
from navi_shell import get_user, print_message

command = "hello"
use = "Say hello"
aliases = ['hi']


def run(arguments=None):
    print_message(f"Hi there, {get_user()}!")
