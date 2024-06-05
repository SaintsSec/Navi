#!/bin/python3
"""Recon module."""

import os
import time
import getpass
from mods import mods
from fpdf import FPDF
import pyfiglet
import click
from navi_shell import get_ai_name

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
    target_ip = input(f"{get_ai_name()} [!] - Give me an IP or URL to scan => ")
    scan_options = input(
        f"\n{get_ai_name()} {nMapCommands}\n{get_ai_name()} [!!] - What type of scan (ex: -sV) => ")
    print("\nReport Setup:")
    report_path = input(
        f"{get_ai_name()} [!] - Where do you want to save the report(ex: ~/Cases): ")
    os.system(f'mkdir {report_path}')
    report_name = input(f"{get_ai_name()} [!] - Save report as(ex: Report1) => ")
    full_path = f"{report_path}/{report_name}-{timestr}.txt"
    print("\n" + breakline)

    # Scan execution
    print("\nThe Process:")
    print(f"{get_ai_name()} [!] - Pinging host to see if its alive...")
    os.system(f'ping -c 4 {target_ip} >> {full_path}')
    os.system(f'echo {breakline} >> {full_path}')
    print(f"{get_ai_name()} [\u2713] - Ping scan complete!")
    time.sleep(2)

    # Nmap Execution
    print(f"{get_ai_name()} [!] - Starting Scan now: nmap {scan_options} {target_ip}")
    os.system(f"nmap {scan_options} {target_ip} >> {full_path}")
    print(f"{get_ai_name()} [\u2713] - nmap scan complete!!")
    time.sleep(2)

    # Whois
    print(f"{get_ai_name}> [!] - Looking into {target_ip} now!")
    os.system(f"echo {breakline} >> {full_path}")
    os.system(f"whois {target_ip} >> {full_path}")
    print(f"{get_ai_name()} [\u2713] - Whois on {target_ip} complete")

    # Report loop
    report_choice = input(f"\n{get_ai_name()} [\u2713] - RECON COMPLETE \nDo you want to see the report now? (yes / no) => ").lower()
    if report_choice == "yes":
        print(f"\n{get_ai_name()} [\u2713] - Showing generated report now!")
        print(f"\n[!]View this report anytime at: {full_path}[!!]")
        print("\n" + breakline)
        time.sleep(2)
        os.system(f"cat {full_path}")
        input(f"\n{get_ai_name()} Press Enter to return to main chat")
    elif report_choice == "no":
        print(f"\n{get_ai_name()} [\u2713] - That is fair. \nReport contents saved to: {full_path}\n\n")
        input(f"\n{get_ai_name()} Press Enter to return to main chat")
    else:
        print(f"\n{get_ai_name()} [!] - The report can be viewed at: {full_path}\n\n")
        input(f"\n{get_ai_name()} Press enter to return to main chat")
        return
