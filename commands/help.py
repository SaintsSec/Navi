#!/bin/python3
import subprocess, os, importlib_metadata, importlib 
from typing import List
from navi_shell import tr, get_ai_name, llm_chat, get_user
from navi import get_ip_address, get_hostname, get_parameters, get_command_path


command = "Navi Help"
use = "Displays the help screen"
aliases = ['help']


def run(arguments=None):


    directory_path = '/opt/Navi/commands'

    commands_and_uses = []



    files = [f for f in os.listdir(directory_path) if f.endswith('py') and f != '__init__.py']

    for file in files:


        command = file.replace('.py', '')


         # Load the module
        spec = importlib.util.spec_from_file_location(command, os.path.join(directory_path, file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

         # Grab the 'use' variable from the module
         # Default to 'Description not found' if 'use' is not in the script
        use_desc = getattr(module, 'use', 'Description not found')
        aliases = getattr(module, 'aliases', 'aliases not found')

        commands_and_uses.append((command, use_desc, aliases))



    max_command_length = 0
    max_use_length = 0
    max_alias_length = 0

    for command, use_desc, aliases in commands_and_uses:


        if len(command) > max_command_length:
            max_command_length = len(command)

        if len(use_desc) > max_use_length:
            max_use_length = len(use_desc)

        if len(' '.join(aliases)) > max_alias_length:
            max_alias_length = len(' '.join(aliases))

    print("\nCurrently installed Navi custom scripts:\n")
    print(f"{'Command':<{max_command_length}} {'Description':^{max_use_length}} {'Aliases':^{max_alias_length}}")  # Add headers
    print("-" * (max_command_length + max_use_length + 2) + "-" * (max_alias_length + 1))  # Add separator

    for command, use_desc, aliases in commands_and_uses:

        print(f"{command:<{max_command_length}} \t {use_desc:<{max_use_length}} {aliases}")
    print("\nHELP: To use any of these commands simply type the alias into \nthe user prompt and run the coresponding script!")
    print("-" * (max_command_length + max_use_length + 2) + "-" * (max_alias_length + 1))  # Add separator

    return None
