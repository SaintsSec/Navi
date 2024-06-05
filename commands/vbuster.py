#!/bin/python3

# TODO - Add rkhunter

import os
from mods import mods
import pyfiglet
import click
from navi_shell import pre_run

command = "vbuster"
use = "Virus removal suite"

# global variables
breakline = mods.breakline


def header_art():
    header = pyfiglet.figlet_format("VBuster", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


def run(arguments=None):
    pre_run()
    header_art()
    # Setup
    scan_options = input(
        "Navi> What options do you want to scan with (ex: -r)\n=> ")
    scan_dir = input("Navi> Where do you want to scan (ex: ~/)\n=> ")
    output_choice = input(
        "Navi> Do you want to save a report (yes/no)\n=> ").lower()
    if output_choice == "yes":
        output_dir = input(
            "Navi> Where do you want you save the report(ex: vbusterOut)\n=>  ")
        output_name = input(
            "Navi> What do you want the report to be called (ex: testReport)\n=> ")
        os.system(f"mkdir {output_dir}")
        os.system(f"touch {output_dir}/{output_name}.txt")
        print("Navi> [!] - Starting scan now... Just a sec.")
        # Start
        os.system(
            f"clamscan {scan_options} {scan_dir} >> {output_dir}/{output_name}.txt")
        viewreport = input(
            "Navi> Scan Complete do you want to see the report now (yes/no)\n=> ").lower()
        if viewreport == "yes":
            os.system(f"cat {output_dir}/{output_name}.txt\n{breakline}\n")
            input("\nNavi> Press enter to return to chat.")
        elif viewreport == "no":
            print(
                f"Navi> Understood, the report can be viewed at: {output_dir}/{output_name}.txt \n{breakline}\n")
            input("\nNavi> Press enter to return to chat.")
        else:
            print(f"Navi> Invalid option... Try again...\n{breakline}\n")
    elif output_choice == "no":
        print("Navi> Understood, starting scan now!")
        os.system(f"clamscan {scan_options} {scan_dir}")
        print(f"Navi> Scan complete! Results above! \n{breakline}\n")
        input("\nNavi> Press enter to return to chat")
    else:
        print(f"Navi> Invalid option! Try again! \n{breakline}\n")
