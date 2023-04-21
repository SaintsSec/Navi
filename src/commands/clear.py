"""Clear Screen module."""

from mods import mods

command = "/clear"
use = "clears the screen"

art = mods.art

def run():
    """Clearing Screen."""
    mods.clearScreen()
    print(art)
