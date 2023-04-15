"""Clear Screen module."""

import os

command = "/clear"
use = "clears the screen"

def run():
    """Clearing Screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

