# Imports.
import sys # System stuff.
import os # Operating System functions.
from colorama import Fore # For text colour.

# Pre-run.
#os.system("clear")

# Hide tracebacks - change to 1 for dev mode.
sys.tracebacklimit = 0

# Config (Prints).
print_text = (f"{Fore.WHITE}") # Change the colour of text output in the client side prints.
print_dividers = (f"{Fore.LIGHTRED_EX}") # Changes the [], | and : in the client side prints.
print_success = (f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}]") # Success output.
print_successfully = (f"{Fore.WHITE}[{Fore.GREEN}SUCCESSFULLY{Fore.WHITE}]") # Successfully output.
print_failed = (f"{Fore.WHITE}[{Fore.LIGHTRED_EX}FAILED{Fore.WHITE}]") # Failed output.
print_prompt = (f"{Fore.WHITE}[{Fore.YELLOW}»{Fore.WHITE}]") # Prompt output.
print_notice = (f"{Fore.WHITE}[{Fore.YELLOW}!{Fore.WHITE}]") # Notice output.
print_question =  (f"{Fore.WHITE}[{Fore.YELLOW}?{Fore.WHITE}]") # Alert output.
print_alert =  (f"{Fore.WHITE}[{Fore.LIGHTRED_EX}!{Fore.WHITE}]") # Alert output.
print_exited = (f"{Fore.WHITE}[{Fore.LIGHTRED_EX}EXITED{Fore.WHITE}]") # Execited output.
print_disconnected = (f"{Fore.WHITE}[{Fore.LIGHTRED_EX}DISCONNECTED{Fore.WHITE}]") # Disconnected output.
print_command = (f"\n[{Fore.YELLOW}>_{Fore.WHITE}]: ") # Always asks for a command on a new line.

# Program.
try:
    print("\n") # Gaps the text.
    print(f"{print_question} What hccapx file are you attacking?\n(Currently Netgear and must be WPA-PBKDF2-PMKID+EAPOL)\n")
    capture = input(f"{print_command} ")
    print(f"{print_question} What wordlist would you like to run?\n") # Preferable to state the full working directory.
    wl = input(f"{print_command} ")
    print("\n")
    os.system(f"hashcat -d1 -m 22000 -w3 --status -a6 ./captures/{capture} ./wldb/{wl} ?d?d?d")
    print(f"\n{print_exited} {print_notice} {print_successfully}\n") # States the script ended.

# Error handling.
except KeyboardInterrupt:
    print("\n") # Gaps the print.
    print(f"{print_exited} {print_notice} {print_successfully}") # States the script ended.
    print("\n") # Gaps the print.
    print(f'{print_notice} You interrupted the program.') # States it was interrupted.
    print("\n") # Gaps the print.
    try:
        sys.exit(0) # Attempts to exit.
    except SystemExit:
        os._exit(0) # Attempts to exit.
except ValueError:
    print("\n") # Gaps the print.
    print(f"{print_exited} {print_notice} {print_successfully}") # States the script ended.
    print("\n") # Gaps the print.
    print(f'{print_notice} You entered invalid data into a field.') # States it was interrupted.
    print("\n") # Gaps the print.
    try:
        sys.exit(0) # Attempts to exit.
    except SystemExit:
        os._exit(0) # Attempts to exit.
