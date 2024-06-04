#!/bin/python3

# TODO - Add rkhunter

# imports
import os
from mods import mods
import pyfiglet
import click 

command = "vbuster"
use = "Virus removal suite"

# global variables
breakline = mods.breakline

def headerArt():
    header = pyfiglet.figlet_format("VBuster", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def run(arguments = None):
    clear_screen()
    headerArt()
    # Setup
    scanOptions = input(
        "Navi> What options do you want to scan with (ex: -r)\n=> ")
    scanDir = input("Navi> Where do you want to scan (ex: ~/)\n=> ")
    outputChoice = input(
        "Navi> Do you want to save a report (yes/no)\n=> ").lower()
    if outputChoice == "yes":
        outputDir = input(
            "Navi> Where do you want you save the report(ex: vbusterOut)\n=>  ")
        outputName = input(
            "Navi> What do you want the report to be called (ex: testReport)\n=> ")
        os.system(f"mkdir {outputDir}")
        os.system(f"touch {outputDir}/{outputName}.txt")
        print("Navi> [!] - Starting scan now... Just a sec.")
        # Start
        os.system(
            f"clamscan {scanOptions} {scanDir} >> {outputDir}/{outputName}.txt")
        viewReport = input(
            "Navi> Scan Complete do you want to see the report now (yes/no)\n=> ").lower()
        if viewReport == "yes":
            os.system(f"cat {outputDir}/{outputName}.txt\n{breakline}\n")
            input("\nNavi> Press enter to return to chat.")
        elif viewReport == "no":
            print(
                f"Navi> Understood, the report can be viewed at: {outputDir}/{outputName}.txt \n{breakline}\n")
            input("\nNavi> Press enter to return to chat.")
        else:
            print(f"Navi> Invalid option... Try again...\n{breakline}\n")
    elif outputChoice == "no":
        print("Navi> Understood, starting scan now!")
        os.system(f"clamscan {scanOptions} {scanDir}")
        print(f"Navi> Scan complete! Results above! \n{breakline}\n")
        input("\nNavi> Press enter to return to chat")
    else:
        print(f"Navi> Invalid option! Try again! \n{breakline}\n")
