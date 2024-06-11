#!/bin/python3
import subprocess
from navi_shell import get_ai_name, tr
from navi import get_command_path

command = "navi_sys"
use = "Execute system command created by Navi"


def run(arguments=None):
    navi_command = arguments.replace("TERMINAL OUTPUT", "", 1).strip()
    base_command = navi_command.split()[0]
    if get_command_path(base_command) is not None:
        tr(f"\n{get_ai_name()} To fulfill your request, I will have to utilize your **shell** to execute the following: {navi_command}."
           f" Do you want me to proceed? (y/n): ")
        user_input = input().strip().lower()
        if user_input == 'y':
            result = subprocess.run(
                navi_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            tr(f"\n{get_ai_name()} Done! Output: {result.stdout}")
        else:
            tr(f"\n{get_ai_name()} Understood! I will not execute the command.")
    else:
        tr(f"\n{get_ai_name()} Sorry, it looks like {command} is not installed on your system.")