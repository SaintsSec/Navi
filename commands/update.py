import os
import pyfiglet
import click
from navi_shell import get_latest_release

command = "update"
use = "Updates navi"
ai_name_rep = "Navi>"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def headerArt():
    header = pyfiglet.figlet_format("Navi Updates", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


def run(arguments=None):
    clear_screen()
    headerArt()
    get_latest_release()
