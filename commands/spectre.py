#!/bin/python3
"""Recon module."""

import os
import time
import getpass
from mods import mods
from fpdf import FPDF
import pyfiglet
import click 
command = "/spectre"
use = "Recon automation suite"

# Global Vars
breakline = mods.breakline
nMapCommands = mods.nMapCommands
timestr = time.strftime("%m%d%Y-%H:%M")
pdf = FPDF()
user = getpass.getuser()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def headerArt():
    header = pyfiglet.figlet_format("Spectre Recon", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


pdf.add_page()
pdf.set_font("Arial", size=10)


def run():
    """Do recon."""
    # Recon Setup
    clear_screen()
    headerArt()
    print("\nNmap Setup:")
    targetIP = input("Navi> [!] - Give me an IP or URL to scan => ")
    scanOptions = input(
        f"\nNavi> {nMapCommands}\nNavi> [!!] - What type of scan (ex: -sV) => ")
    print("\nReport Setup:")
    reportPath = input(
        "Navi> [!] - Where do you want to save the report(ex: ~/Cases): ")
    os.system(f'mkdir {reportPath}')
    reportName = input("Navi> [!] - Save report as(ex: Report1) => ")
    fullPath = f"{reportPath}/{reportName}-{timestr}.txt"
    print("\n" + breakline)

    # Scan execution
    print("\nThe Process:")
    print("Navi> [!] - Pinging host to see if its alive...")
    os.system(f'ping -c 4 {targetIP} >> {fullPath}')
    os.system(f'echo {breakline} >> {fullPath}')
    print("Navi> [\u2713] - Ping scan complete!")
    time.sleep(2)

    # Nmap Execution
    print(f"Navi> [!] - Starting Scan now: nmap {scanOptions} {targetIP}")
    os.system(f"nmap {scanOptions} {targetIP} >> {fullPath}")
    print("Navi> [\u2713] - nmap scan complete!!")
    time.sleep(2)

    # Whois
    print(f"Navi> [!] - Looking into {targetIP} now!")
    os.system(f"echo {breakline} >> {fullPath}")
    os.system(f"whois {targetIP} >> {fullPath}")
    print(f"Navi> [\u2713] - Whois on {targetIP} complete")

    # Report loop
    reportChoice = input(
        "\nNavi> [\u2713] - RECON COMPLETE \nDo you want to see the report now? (yes / no) => ").lower()
    if reportChoice == "yes":
        print("\nNavi> [\u2713] - Showing generated report now!")
        print(f"\n[!]View this report anytime at: {fullPath}[!!]")
        print("\n" + breakline)
        time.sleep(2)
        os.system(f"cat {fullPath}")
        input("\nNavi> Press Enter to return to main chat")
    elif reportChoice == "no":
        print(
            f"\nNavi> [\u2713] - That is fair. \nReport contents saved to: {fullPath}\n\n")
        input("\nNavi> Press Enter to return to main chat")
    else:
        print(f"\nNavi> [!] - The report can be viewed at: {fullPath}\n\n")
        input("\nNavi> Press enter to return to main chat")
        return
