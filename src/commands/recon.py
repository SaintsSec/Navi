"""Recon module."""

import os
import time
from mods import mods

command = "/recon"
use = "Recon automation suite"

#Global Vars
breakline = mods.breakline
nMapCommands = mods.nMapCommands
timestr = time.strftime("%m%d%Y-%H:%M")

def run():
    """Do recon."""
    # Recon Setup
    print("\nNmap Setup:")
    targetIP = input("Navi> [!] - Give me an IP or URL to scan => ")
    scanOptions = input(f"\nNavi> {nMapCommands}\nNavi> [!!] - What type of scan (ex: -sV) => ")
    print("\nReport Setup:")
    reportName = input("Navi> [!] - Save report as(ex: Report1) => ")
    os.system(f'touch ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt')
    print("\n" + breakline)
    
    # Scan execution
    print("\nThe Process:")
    print("Navi> [!] - Pinging host to see if its alive...")
    os.system(f'ping -c 4 {targetIP} >> ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt')
    os.system(f'echo {breakline} >> ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt')
    print("Navi> [\u2713] - Ping scan complete!")
    time.sleep(2)

    #Nmap Execution
    print(f"Navi> [!] - Starting Scan now: nmap {scanOptions} {targetIP}")
    os.system(f"nmap {scanOptions} {targetIP} >> ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt")
    print("Navi> [\u2713] - nmap scan complete!!")
    time.sleep(2)
    
    #Whois
    print(f"Navi> [!] - Looking into {targetIP} now!")
    os.system(f"echo {breakline} >> ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt")
    os.system(f"whois {targetIP} >> ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt")
    print(f"Navi> [\u2713] - Whois on {targetIP} complete")

    #Report loop
    reportChoice = input("\nNavi> [\u2713] - RECON COMPLETE \nDo you want to see the report now? (yes / no) => ").lower()
    if reportChoice == "yes":
        print("\nNavi> [\u2713] - Showing generated report now!")
        print(f"\n[!]View this report anytime at: ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt[!!]")
        print("\n" + breakline)
        time.sleep(2)
        os.system(f"cat ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt")
    if reportChoice == "no":
        print(f"\nNavi> [\u2713] - That is fair. \nReport contents saved to: ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt\n\n")
        return
    else:
        print(f"\nNavi> [!] - The report can be viewed at: ~/Documents/NaviReports/Navi-{timestr}-{reportName}.txt\n\n")
        return
