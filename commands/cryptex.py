import sys
from .app_cryptex.controller import Controller
from .app_cryptex.menusystem import MenuSystem
from navi import get_parameters
from navi_shell import tr
from .app_cryptex.cipher.ciphers import *

command = "cryptex"
use = "An advanced command-line cryptography toolkit"


args_dict = {
    "cipher": {"type": str, "help": "The cipher name", "nargs": "?"},
    "-e": {"alias": "--encode", "dest": "encode", "action": "store_true", "help": "Encode mode"},
    "-d": {"alias": "--decode", "dest": "decode", "action": "store_true", "help": "Decode mode"},
    "--test": {"dest": "test", "action": "store_true", "help": "Run all tests"},
    "-b": {"alias": "--brute", "dest": "brute", "action": "store_true", "help": "Brute mode"},
    "-t": {"alias": "--text", "dest": "text", "type": str, "help": "The input text"},
    "-k": {"alias": "--key", "dest": "key", "type": str, "help": "The key"},
    "-ex": {"alias": "--exclude", "dest": "exclude", "type": str, "help": "The exclude list"},
    "-o": {"alias": "--output", "dest": "output", "type": str, "help": "output file"},
    "-i": {"alias": "--input", "dest": "input", "type": str, "help": "input file"},
    "-iw": {"alias": "--imageWidth", "dest": "imageWidth", "type": int, "help": "image width"},
    "-m": {"alias": "--monocromatic", "dest": "monocromatic", "action": "store_true", "help": "monocromatic"},
    "-lang": {"dest": "languages", "action": "store_true", "help": "show languages"},
    "-src": {"dest": "src_lang", "type": str, "help": "source language"},
    "-dest": {"dest": "dest_lang", "type": str, "help": "destination language"},
    "-len": {"dest": "length", "type": int, "help": "length"},
    "-ka": {"alias": "--key_a", "dest": "key_a", "type": int, "help": "Key -a"},
    "-kb": {"alias": "--key_b", "dest": "key_b", "type": int, "help": "Key -b"},
    "-r": {"alias": "--range", "dest": "range", "type": str, "help": "Range"}
}


def check_argument(args, name):
    for index, arg in enumerate(args):
        for key, value in args_dict.items():
            if key == arg or value.get("alias") == arg:
                if value.get("dest") == name:
                    return index, value
    return False


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
        return

    # Start the menu if specified
    if '--tui' in argv[1] or '-tui' in argv[1]:
        MenuSystem(cipher_list)
        return

    # Start the controller
    controller.run(argv)
