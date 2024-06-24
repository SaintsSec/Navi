#!/bin/python3
import re
import subprocess
from typing import List
from navi_shell import tr, llm_chat
from navi import get_ip_address, get_hostname, get_command_path

command = "nmap"
use = "Port scanning"


def run_nmap_scan(target, ports=None, arguments=None):
    # Initialize the nmap command
    command_construction = ['nmap']
    if ports:
        command_construction.extend(['-p', ','.join(ports)])  # Join the ports list into a single string
    if arguments:
        command_construction.extend(arguments)
    command_construction.append(target)

    # Ensure all elements in the command are strings and strip whitespace
    command_construction = [str(arg).strip() for arg in command_construction]

    # Run the nmap command
    result = subprocess.run(
        command_construction,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    return result.stdout, result.stderr


def get_nmap_parameters(input_str):
    pattern = re.compile(r"""
        -p\s*[\d,-]+|                     # Match -p followed by digits, commas, or hyphens (port ranges)
        -[A-Za-z0-9]{1,2}(?:\s|$)|        # Match short flags (e.g., -A, -sV) followed by a space or end of string
        --\w+(?:=\S+)?|                   # Match long flags and their arguments (e.g., --script, --version-intensity=5)
        \b-T[0-5]\b                       # Match timing templates (e.g., -T0 to -T5)
    """, re.VERBOSE)


def run(arguments=None):
    if get_command_path(command) is None:
        tr(f"\nSorry! nmap is not currently installed on your system.")
        return
    ip_address = None
    hostname = None

    port_numbers: List[str] = []
    if arguments:
        for token in arguments:
            if (ip_address := get_ip_address(token.text)) or (hostname := get_hostname(token.text)):
                break

        # Find multiple port numbers
        ports_pattern = re.compile(r'\bports?\s+([\d\s,]+(?:\s*(?:and|,)\s*[\d\s,]*)*)', re.IGNORECASE)
        for match in ports_pattern.finditer(arguments.text):
            ports_text = match.group(1)
            # Split ports by 'and', commas, and spaces to handle multiple ports
            for port in re.split(r'\s*,\s*|\s+and\s+|\s+', ports_text):
                if port.isdigit():
                    port_numbers.append(port)
    if ip_address is None and hostname is None:
        tr(f"\nSorry, you need to provide a valid IP address or hostname")
    else:
        tr(f"\nRunning... hang tight!")
        target = ip_address if ip_address is not None else hostname
        matches = get_nmap_parameters(arguments.text)
        stdout, stderr = run_nmap_scan(target, port_numbers, matches)

        # Ask user how they want to handle the results
        choice = input(f"\nScan done! Would you like me to analyze the results or just see the raw "
                       f"output? (type 'analyze' or 'raw'): ").strip().lower()

        if choice == 'analyze':
            response_message, http_status = llm_chat(f"Please analyze and summarize the results of "
                                                     f"this nmap scan: {stdout}")
            tr(f"{response_message if http_status == 200 else f'Issue with server. '}{f'Here are the results: {stdout}'}")
        elif choice == 'raw':
            tr(f"\nHere are the raw results:\n{stdout}")
        else:
            tr("Invalid choice. Showing raw results by default.\n")
            tr(f"\nHere are the raw results:\n{stdout}")
