"""Help command."""

import commands
from mods import mods

breakline = mods.breakline
command = "/help"
use = "Displays a help message"


def run():
    """Show help menu."""
    print("""
Navi Help Menu:
Navi is a simple to use GPT bot that focuses in on assisting with
tasks related to the field of cybersecurity.
[!!] - All commands are preceeded by a '/'
Here is a list of current useable commands:

Command:              Use:""")
    for _, module in commands.modules.items():
        print(module.command.ljust(21), module.use)
