import sys
from .app_cryptex.controller import Controller
from .app_cryptex.menusystem import MenuSystem
from navi import get_parameters

command = "cryptex"
use = "An advanced command-line cryptography toolkit"


def run(arguments=None):
    # Check if there are args
    argv = get_parameters(arguments.text)
    argv.pop(0)  # Remove the command name

    # Gather ciphers
    from .app_cryptex.cipher.cipher import Cipher
    cipher_list = {cls.__name__.lower(): cls for cls in Cipher.__subclasses__()}

    # Initialize cipher
    controller = Controller(cipher_list)

    # If there are no args, exit.
    if not argv:
        controller.cli.print_ciphers()
        tr("Please enter an argument when using this command.\nTry --help or -h for more information")

    # Start the menu if specified
    if '--tui' in argv[1] or '-tui' in argv[1]:
        MenuSystem(cipher_list)
        return

    # Start the controller
    controller.run(argv)
