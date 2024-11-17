#!/bin/python3
import navi_internal
import sys
import os
from colorama import Fore

command: str = "chip-create"
use: str = "Creates a new Navi chip"
aliases: list = ['chip-create', 'cc']
params: dict = {
    '-help': 'Display help information',
    '-h': 'Display help information',
}

help_params: tuple = ('-help', '-h')
template_file: str = "chips/SSG/chip-template.txt"
chip_install_path: str = "chips/Dev/"
chip_file_path: str = ""
chip_documentation_link: str = "https://github.com/SaintsSec/Navi/wiki/4.-Developing-Chips-%E2%80%90-Indepth"


def print_params() -> None:
    # Print the header
    print(f"{'Parameter':<10} | {'Description'}")
    print("-" * 40)

    # Print each dictionary item
    for param, description in params.items():
        print(f"{param:<10} | {description}")


def run(arguments=None) -> None:
    navi_instance = navi_internal.navi_instance
    arg_array = arguments.text.split()
    arg_array.pop(0)
    if arg_array is not None:
        for arg in arg_array:
            match arg:
                case x if x in help_params:
                    print_params()
                    return
                case _:
                    navi_instance.print_message(f"Invalid parameter: {arg}\n"
                                                f"Do you want to review the available parameters? (y/n): ")
                    choice = input().strip().lower()
                    if choice == 'y':
                        print_params()
                        return
                    return

    navi_instance.print_message(
        f"Welcome to Navi chip creator, {navi_instance.get_user()}. Please enter the name of your new Chip.")
    chip_name = input("Chip Name: ")

    # Ask for the file name
    navi_instance.print_message(
        f"Great name, {navi_instance.get_user()}! What do you want the python file to be called?")
    chip_file_name = input("Chip File Name: ")
    while True:
        # Recap the entered information
        navi_instance.print_message(f"Perfect! Here's a recap:"
                                    f"\nChip Name: {chip_name}"
                                    f"\nPython File Name: {chip_file_name}.py\n")

        while True:  # Loop to ensure valid input for continue/make changes
            # Ask the user if they want to proceed or make changes
            choice = input("Are you ready to proceed or do you want to make changes? "
                           f"({Fore.YELLOW}c{Fore.RESET})ontinue or ({Fore.YELLOW}m{Fore.RESET})ake changes: ").strip().lower()

            if choice == 'c':
                navi_instance.print_message("Awesome! Moving forward with the given details.")
                break  # Exit the input validation loop
            elif choice == 'm':
                while True:  # Loop to ensure valid input for what to change
                    # Ask the user what they want to change
                    change_choice = input(f"What do you want to change? ({Fore.YELLOW}chip{Fore.RESET}) name or "
                                          f"({Fore.YELLOW}file{Fore.RESET}) name: ").strip().lower()

                    if change_choice == 'chip':
                        navi_instance.print_message("Let's update the Chip Name.")
                        chip_name = input("New Chip Name: ")
                        break  # Exit the loop for change choice
                    elif change_choice == 'file':
                        navi_instance.print_message("Let's update the File Name.")
                        chip_file_name = input("New File Name: ")
                        break  # Exit the loop for change choice
                    else:
                        navi_instance.print_message("Invalid choice. Please enter 'chip' or 'file'.")

                break  # Exit the input validation loop and recap changes
            else:
                navi_instance.print_message("Invalid input. Please choose 'c' to continue or 'm' to make changes.")
        if choice == 'c':
            break

    # Check if the template file exists
    if os.path.exists(template_file):
        with open(template_file, "r") as template:
            template_content = template.read()

        # Replace placeholders in the template if needed (optional)
        chip_file_name_final = chip_file_name.replace(".py", "") + ".py"
        template_content = template_content.replace("{{CHIP_NAME}}", chip_name)
        # Write the content to the new file
        chip_file_path = os.path.join(os.getcwd(), chip_install_path + chip_file_name_final)
        with open(chip_file_path, "w") as chip_dev:
            chip_dev.write(template_content)

        navi_instance.print_message(f"{Fore.GREEN}Chip '{chip_name}' created successfully!{Fore.RESET}")
    else:
        navi_instance.print_message(f"{Fore.RED}ERROR:{Fore.RESET} Template file '{template_file}' is missing. Aborting.")

    navi_instance.print_message(f"Here are some options for you:\n"
                                f"{Fore.YELLOW}1{Fore.RESET}: Open directory of Chip location\n"
                                f"{Fore.YELLOW}2{Fore.RESET}: Open in your preferred code editor\n"
                                f"{Fore.YELLOW}3{Fore.RESET}: Reload Navi to load the new Chip\n"
                                f"{Fore.YELLOW}4{Fore.RESET}: Review the documentation online\n"
                                f"{Fore.YELLOW}5{Fore.RESET} or other value: I'm finished")
    choice = input("Please enter 1, 2, 3, 4, or 5: ")
    match choice:
        case '1':
            print("Opening directory of Chip location")
        case '2':
            print("Opening in your preferred code editor")
            import subprocess
            try:
                if sys.platform == 'win32':
                    os.startfile(chip_file_path)
                elif sys.platform == 'darwin':
                    subprocess.call(['open', chip_file_path])
                else:
                    subprocess.call(['xdg-open', chip_file_path])
            except Exception as e:
                print(f"Failed to open the log file: {e}")
        case '3':
            navi_instance.reload()
        case '4':
            import webbrowser
            webbrowser.open(chip_documentation_link)
        case _:
            return
