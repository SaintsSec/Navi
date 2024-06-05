#!/bin/python3

# TODO - Add rkhunter

import os
from mods import mods
import pyfiglet
import click
from navi_shell import pre_run,get_ai_name

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
        f"{get_ai_name()} What options do you want to scan with (ex: -r)\n=> ")
    scan_dir = input(f"{get_ai_name()} Where do you want to scan (ex: ~/)\n=> ")
    output_choice = input(
        f"{get_ai_name()} Do you want to save a report (yes/no)\n=> ").lower()
    if output_choice == "yes":
        output_dir = input(
            f"{get_ai_name()} Where do you want you save the report(ex: vbusterOut)\n=>  ")
        output_name = input(
            f"{get_ai_name()} What do you want the report to be called (ex: testReport)\n=> ")
        os.system(f"mkdir {output_dir}")
        os.system(f"touch {output_dir}/{output_name}.txt")
        print(f"{get_ai_name()} [!] - Starting scan now... Just a sec.")
        # Start
        os.system(
            f"clamscan {scan_options} {scan_dir} >> {output_dir}/{output_name}.txt")
        viewreport = input(
            f"{get_ai_name()} Scan Complete do you want to see the report now (yes/no)\n=> ").lower()
        if viewreport == "yes":
            os.system(f"cat {output_dir}/{output_name}.txt\n{breakline}\n")
            input(f"\n{get_ai_name()} Press enter to return to chat.")
        elif viewreport == "no":
            print(
                f"{get_ai_name()} Understood, the report can be viewed at: {output_dir}/{output_name}.txt \n{breakline}\n")
            input(f"\n{get_ai_name()} Press enter to return to chat.")
        else:
            print(f"{get_ai_name()} Invalid option... Try again...\n{breakline}\n")
    elif output_choice == "no":
        print(f"{get_ai_name()} Understood, starting scan now!")
        os.system(f"clamscan {scan_options} {scan_dir}")
        print(f"{get_ai_name()} Scan complete! Results above! \n{breakline}\n")
        input(f"\n{get_ai_name()} Press enter to return to chat")
    else:
        print(f"{get_ai_name()} Invalid option! Try again! \n{breakline}\n")
