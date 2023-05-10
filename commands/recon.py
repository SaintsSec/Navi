"""Recon module."""

import os
import time
from mods import mods
from fpdf import FPDF

command = "/recon"
use = "Recon automation suite"

#Global Vars
breakline = mods.breakline
nMapCommands = mods.nMapCommands
timestr = time.strftime("%m%d%Y-%H:%M")
pdf = FPDF()

pdf.add_page()
pdf.set_font("Arial", size = 10)

def run():
    """Do recon."""
    # Recon Setup
    print("\nNmap Setup:")
    targetIP = input("Navi> [!] - Give me an IP or URL to scan => ")
    scanOptions = input(f"\nNavi> {nMapCommands}\nNavi> [!!] - What type of scan (ex: -sV) => ")
    print("\nReport Setup:")
    reportPath = input(f"Navi> [!] - Where do you want to save the report(ex: ~/Cases): ")
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

    #Nmap Execution
    print(f"Navi> [!] - Starting Scan now: nmap {scanOptions} {targetIP}")
    os.system(f"nmap {scanOptions} {targetIP} >> {fullPath}")
    print("Navi> [\u2713] - nmap scan complete!!")
    time.sleep(2)
    
    #Whois
    print(f"Navi> [!] - Looking into {targetIP} now!")
    os.system(f"echo {breakline} >> {fullPath}")
    os.system(f"whois {targetIP} >> {fullPath}")
    print(f"Navi> [\u2713] - Whois on {targetIP} complete")

    #Report loop
    reportChoice = input("\nNavi> [\u2713] - RECON COMPLETE \nDo you want to see the report now? (yes / no) => ").lower()
    if reportChoice == "yes":
        print("\nNavi> [\u2713] - Showing generated report now!")
        print(f"\n[!]View this report anytime at: {fullPath}[!!]")
        print("\n" + breakline)
        time.sleep(2)
        os.system(f"cat {fullPath}")
    if reportChoice == "no":
        print(f"\nNavi> [\u2713] - That is fair. \nReport contents saved to: {fullPath}\n\n")
    else:
        print(f"\nNavi> [!] - The report can be viewed at: {fullPath}\n\n")

    #convert to pdf:
    pdfChoice = input(f"{breakline}\n\nNavi> [!] - Would you like to export {reportName} into a pdf? (yes / no): ").lower()
    if pdfChoice == "yes":
        file = open(f"{reportPath}/{reportName}-{timestr}.txt", "r")
        for x in file:
            pdf.cell(2000, 5, txt = x, ln = 1)
        pdf.output(f"{reportPath}/{reportName}-{timestr}.pdf")
        print(f"Navi> [\u2713] - pdf generated it can be found at: {reportPath}/{reportName}-{timestr}.pdf")
    if pdfChoice == "no":
        print("Navi> [!] - Understood cracking on!")
        return
    else:
        print("Navi> [!] - Not a valid option. Moving on...")
        return
