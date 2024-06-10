#!/bin/python3
import re
import subprocess
from typing import List
from navi_shell import tr, get_ai_name, llm_chat

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


def run(arguments=None):
    ip_address = None
    hostname = None

    port_numbers: List[str] = []
    if arguments:
        for token in arguments:
            # Find IP address using regex match
            if re.match(r'(\d{1,3}\.){3}\d{1,3}', token.text):
                ip_address = token.text
            # Find hostname using regex match
            elif re.match(r'[a-zA-Z0-9\-]+\.[a-zA-Z]{2,3}', token.text):
                hostname = token.text

        # Find multiple port numbers
        ports_pattern = re.compile(r'\bports?\s+([\d\s,]+(?:\s*(?:and|,)\s*[\d\s,]*)*)', re.IGNORECASE)
        for match in ports_pattern.finditer(arguments.text):
            ports_text = match.group(1)
            # Split ports by 'and', commas, and spaces to handle multiple ports
            for port in re.split(r'\s*,\s*|\s+and\s+|\s+', ports_text):
                if port.isdigit():
                    port_numbers.append(port)
    if ip_address is None and hostname is None:
        tr(f"\n{get_ai_name()} Sorry, you need to provide a valid IP address or hostname")
    else:
        tr(f"\n{get_ai_name()} Running... hang tight!")
        target = ip_address if ip_address is not None else hostname
        pattern = re.compile(r"""
        -p\s*[\d,-]+|                     # Match -p followed by digits, commas, or hyphens (port ranges)
        -[A-Za-z0-9]{1,2}(?:\s|$)|        # Match short flags (e.g., -A, -sV) followed by a space or end of string
        --\w+(?:=\S+)?|                   # Match long flags and their arguments (e.g., --script, --version-intensity=5)
        \b-T[0-5]\b                       # Match timing templates (e.g., -T0 to -T5)
    """, re.VERBOSE)

        # Find all matches in the command string
        matches = pattern.findall(arguments.text)
        stdout, stderr = run_nmap_scan(target, port_numbers, matches)

        # Ask user how they want to handle the results
        choice = input(f"\n{get_ai_name()} Scan done! Would you like me to analyze the results or just see the raw "
                       f"output? (type 'analyze' or 'raw'): ").strip().lower()

        if choice == 'analyze':
            response_message, http_status = llm_chat(f"Please analyze and summarize the results of "
                                                     f"this nmap scan: {stdout}")
            tr(f"{get_ai_name()} {response_message if http_status == 200 else f'Issue with server. '}{f'Here are the results: {stdout}'}")
        elif choice == 'raw':
            tr(f"\n{get_ai_name()} Here are the raw results:\n{stdout}")
        else:
            tr("Invalid choice. Showing raw results by default.\n")
            tr(f"\n{get_ai_name()} Here are the raw results:\n{stdout}")
