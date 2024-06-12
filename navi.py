import re
import platform
import subprocess


def get_command_path(command):
    windows_commands = get_windows_builtin_commands()

    if windows_commands and is_windows_command(command, windows_commands):
        return True

    if platform.python_version() >= "3.12":
        from shutil import which
        return which(command)
    else:
        from distutils.spawn import find_executable
        return find_executable(command)


def is_windows_command(command, windows_commands):
    return command.upper() in (cmd.upper() for cmd in windows_commands)


def get_windows_builtin_commands():
    if platform.system() != "Windows":
        return []
    result = subprocess.run(["help"], capture_output=True, text=True)
    if result.stdout:
        help_text = result.stdout
        # Extract commands from help text
        commands = []
        lines = help_text.splitlines()
        for line in lines:
            # Command names are typically in uppercase and are single words
            match = re.match(r'^[A-Z]+\b', line.strip())
            if match:
                commands.append(match.group(0))
        return commands
    return []


def get_ip_address(input_str):
    if re.match(r'(\d{1,3}\.){3}\d{1,3}', input_str):
        return input_str
    else:
        return None


def get_hostname(input_str):
    if re.match(r'[a-zA-Z0-9\-]+\.[a-zA-Z]{2,3}', input_str):
        return input_str
    else:
        return None


def get_parameters(input_str):
    pattern = re.compile(r"""
        -p\s*[\d,-]+|                     # Match -p followed by digits, commas, or hyphens (port ranges)
        -[A-Za-z0-9]{1,2}(?:\s|$)|        # Match short flags (e.g., -A, -sV) followed by a space or end of string
        --\w+(?:=\S+)?|                   # Match long flags and their arguments (e.g., --script, --version-intensity=5)
        \b-T[0-5]\b                       # Match timing templates (e.g., -T0 to -T5)
    """, re.VERBOSE)

    # Find all matches in the command string
    return pattern.findall(input_str)
