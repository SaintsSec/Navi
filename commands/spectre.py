#!/bin/python3
"""Recon module."""

import os
import time
import getpass
from mods import mods
from fpdf import FPDF
import pyfiglet
import click

command = "spectre"
use = "Recon automation suite"

# Global Vars
breakline = mods.breakline
nMapCommands = mods.nMapCommands
timestr = time.strftime("%m%d%Y-%H:%M")
pdf = FPDF()
user = getpass.getuser()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def header_art():
    header = pyfiglet.figlet_format("Spectre Recon", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


pdf.add_page()
pdf.set_font("Arial", size=10)


def run(arguments = None):
    """Do recon."""
    # Recon Setup
    clear_screen()
    header_art()
    print("\nNmap Setup:")
    target_ip = input("Navi> [!] - Give me an IP or URL to scan => ")
    scan_options = input(
        f"\nNavi> {nMapCommands}\nNavi> [!!] - What type of scan (ex: -sV) => ")
    print("\nReport Setup:")
    report_path = input(
        "Navi> [!] - Where do you want to save the report(ex: ~/Cases): ")
    os.system(f'mkdir {report_path}')
    report_name = input("Navi> [!] - Save report as(ex: Report1) => ")
    full_path = f"{report_path}/{report_name}-{timestr}.txt"
    print("\n" + breakline)

    # Scan execution
    print("\nThe Process:")
    print("Navi> [!] - Pinging host to see if its alive...")
    os.system(f'ping -c 4 {target_ip} >> {full_path}')
    os.system(f'echo {breakline} >> {full_path}')
    print("Navi> [\u2713] - Ping scan complete!")
    time.sleep(2)

    # Nmap Execution
    print(f"Navi> [!] - Starting Scan now: nmap {scan_options} {target_ip}")
    os.system(f"nmap {scan_options} {target_ip} >> {full_path}")
    print("Navi> [\u2713] - nmap scan complete!!")
    time.sleep(2)

    # Whois
    print(f"Navi> [!] - Looking into {target_ip} now!")
    os.system(f"echo {breakline} >> {full_path}")
    os.system(f"whois {target_ip} >> {full_path}")
    print(f"Navi> [\u2713] - Whois on {target_ip} complete")

    # Report loop
    report_choice = input(
        "\nNavi> [\u2713] - RECON COMPLETE \nDo you want to see the report now? (yes / no) => ").lower()
    if report_choice == "yes":
        print("\nNavi> [\u2713] - Showing generated report now!")
        print(f"\n[!]View this report anytime at: {full_path}[!!]")
        print("\n" + breakline)
        time.sleep(2)
        os.system(f"cat {full_path}")
        input("\nNavi> Press Enter to return to main chat")
    elif report_choice == "no":
        print(
            f"\nNavi> [\u2713] - That is fair. \nReport contents saved to: {full_path}\n\n")
        input("\nNavi> Press Enter to return to main chat")
    else:
        print(f"\nNavi> [!] - The report can be viewed at: {full_path}\n\n")
        input("\nNavi> Press enter to return to main chat")
        return
