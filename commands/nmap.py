#!/bin/python3
import re
from typing import List

command = "nmap"
use = "Port scanning"

ip_address = None
port_numbers: List[str] = []


def run(arguments=None):
    port_numbers = []
    if arguments:
        for token in arguments:
            # Find IP address using regex match
            if re.match(r'(\d{1,3}\.){3}\d{1,3}', token.text):
                ip_address = token.text

            # Find multiple port numbers
        ports_pattern = re.compile(r'\bports?\s+(\d{1,5}(?:\s+and\s+\d{1,5})*)', re.IGNORECASE)
        for match in ports_pattern.finditer(arguments.text):
            ports_text = match.group(1)
            # Split ports by 'and' to handle multiple ports
            for port in re.split(r'\s+and\s+', ports_text):
                if port.isdigit():
                    port_numbers.append(port)

    nmap_construction = f"nmap {'-p ' + ','.join(port_numbers) + ' ' if port_numbers else ''}{ip_address}"
    print(nmap_construction)
