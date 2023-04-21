"""Clear Screen module."""

from mods import mods

command = "/clear"
use = "clears the screen"

breakline = mods.breakline
art = mods.art

def run():
    """Clearing Screen."""
    print(breakline)
    print("Navi> [!!] - Rebooting, see you in a second!")
    mods.clearScreen()
    print(art)
