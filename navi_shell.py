import os
import sys
import getpass
import argparse
import traceback
import navi_internal
from navi_updater import check_version, update_script


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    from datetime import datetime
    
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'crash_{timestamp}.log')

    with open(log_file, 'w') as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

    log_file_path = os.path.abspath(log_file)

    print(f"\nDang! Navi crashed. A crash log has been created at:\n{log_file_path}. \n\nYou can create a new Navi GitHub issue here: \nhttps://github.com/SaintsSec/Navi/issues. \n\nThank you for helping us make Navi better!")

    print("\nWould you like to:")
    print("1) Open the crash log")
    print("2) Ignore and close the app")
    choice = input("Please enter 1 or 2: ")

    if choice == '1':
        import subprocess
        try:
            if sys.platform == 'win32':
                os.startfile(log_file_path)
            elif sys.platform == 'darwin':
                subprocess.call(['open', log_file_path])
            else:
                subprocess.call(['xdg-open', log_file_path])
        except Exception as e:
            print(f"Failed to open the log file: {e}")
        print("Closing the application.")

    sys.exit(1)

sys.excepthook = handle_exception

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
        navi_instance.setup_history()
        navi_instance.chat_with_navi()
        navi_instance.print_message(f"How can I help you {user}")
    except KeyboardInterrupt:
        navi_instance.print_message(f"\nKeyboard interrupt has been registered, talk soon {user}!")
        exit(0)

if __name__ == "__main__":
    main()
