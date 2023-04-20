"""Clear Screen module."""

from mods import mods

command = "/clear"
use = "clears the screen"

def run():
    """Clearing Screen."""
    print(breakline)
    print("Navi> [!!] - Rebooting, see you in a second!")
    mods.clearscreen()
    print(art)
