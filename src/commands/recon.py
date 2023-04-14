"""Recon module."""

import os
import time
from mods import mods

command = "/recon"
use = "Recon automation suite"


def run():
    """Do recon."""
    breakline = mods.breakline

    # Recon Setup
    targetIP = input("Navi> Give me an IP to scan: ")
    scanOptions = input("Navi> What type of scan (ex: -sV): ")
    reportName = input("Navi> What would you like to name the report(ex: Report1): ")
    print(breakline + "\n\n")

    # Scan execution
    print("The Process:")
    print("Navi> [!] - Pinging host to see if its alive...")
    os.system(f'ping -c 4 {targetIP} >> ~/{reportName}.txt')
    os.system(f'echo {breakline} >> ~/{reportName}.txt')
    print("Navi> [\u2713] - Ping scan complete!")
    time.sleep(2)
    print(f"Navi> [!] - Starting Scan now: nmap {scanOptions} {targetIP}")
    os.system(f"nmap {scanOptions} {targetIP} >> ~/{reportName}.txt")
    print("Navi> [\u2713] - nmap scan complete!!")
    print("Navi> [\u2713] - Showing generated report now!")
    print(f"Scan can be viwed anytime at: ~/{reportName}.txt")

    # Show nmap report
    print("\n\n" + breakline)
    os.system(f"cat ~/{reportName}.txt")
    print(breakline)
