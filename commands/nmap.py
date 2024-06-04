#!/bin/python3
# imports
import os
import pyfiglet
import click

command = "nmap"
use = "Port scanning"


def header_art():
    header = pyfiglet.figlet_format("nmap", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run():
    clear_screen()
    header_art()
    # Setup
