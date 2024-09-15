import os
import sys
import getpass
import argparse
import traceback
import navi_internal
from navi_updater import check_version, update_script

user = getpass.getuser()

parser = argparse.ArgumentParser(description='Check for new releases and handle updates.')
parser.add_argument('--edge', action='store_true', help='Check for the edge version')
parser.add_argument('--noupdate', action='store_true', help='Do not check for updates')
parser.add_argument('--update', action='store_true', help='Update the script to the latest version if available')
parser.add_argument('--skip-update', action='store_true',
                    help='Skip the update check (used internally to prevent update loop)')
parser.add_argument('--install', action='store_true', help='installs Navi based on the current downloaded version.')

args = parser.parse_args()

def restart_navi() -> None:
    os.execv(sys.executable, [sys.executable] + sys.argv + ["--skip-update"])  # nosec

def main() -> None:
    navi_instance = navi_internal.navi_instance
    if not args.noupdate and not args.skip_update:
        download_url = check_version(args.edge)
        if download_url:
            update_script(download_url)
    if args.install:
        os.system('cd ./install && ./install.sh')
    try:
        navi_instance.setup_navi_vocab()
        navi_instance.set_user(user)
        navi_instance.clear_terminal()
        navi_instance.chat_with_navi()
        navi_instance.print_message(f"How can I help you {user}")
    except KeyboardInterrupt:
        navi_instance.print_message(f"\nKeyboard interrupt has been registered, talk soon {user}!")
        exit(0)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    with open('crash.log', 'a') as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    sys.exit(1)

sys.excepthook = handle_exception

if __name__ == "__main__":
    main()