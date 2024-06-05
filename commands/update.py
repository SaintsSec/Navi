import pyfiglet
import click
from navi_shell import get_latest_release,pre_run

command = "update"
use = "Updates navi"
ai_name_rep = "Navi>"


def header_art():
    header = pyfiglet.figlet_format("Navi Updates", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


def run(arguments=None):
    pre_run()
    header_art()
    get_latest_release()
