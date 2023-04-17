"""Recon module."""

import os
import time
from mods import mods

command = "/recon"
use = "Recon automation suite"

#Global Vars
breakline = mods.breakline

def run():
    """Do recon."""
    # Recon Setup
    print("Nmap Setup:")
    targetIP = input("Navi> Give me an IP to scan: ")
    scanOptions = input("Navi> What type of scan (ex: -sV): ")
    print("WhoIs Setup:")
    targetUrl = input("Navi> What URL should I look into: ")
    reportName = input("Navi> Save report as(ex: Report1): ")
    print(breakline + "\n")
    
    # Scan execution
    print("The Process:")
    print("Navi> [!] - Pinging host to see if its alive...")
    os.system(f'ping -c 4 {targetIP} >> ~/{reportName}.txt')
    os.system(f'echo {breakline} >> ~/{reportName}.txt')
    print("Navi> [\u2713] - Ping scan complete!")
    time.sleep(2)

    #Nmap Execution
    print(f"Navi> [!] - Starting Scan now: nmap {scanOptions} {targetIP}")
    os.system(f"nmap {scanOptions} {targetIP} >> ~/{reportName}.txt")
    print("Navi> [\u2713] - nmap scan complete!!")
    time.sleep(2)
    
    #Whois
    print(f"Navi> [!] - Looking into {targetUrl} now!")
    os.system(f"echo {breakline} >> ~/{reportName}.txt")
    os.system(f"whois {targetUrl} >> ~/{reportName}.txt")
    print(f"Navi> [\u2713] - Whois on {targetUrl} complete")
    time.sleep(2)

    #Show Report
    print("Navi> [\u2713] - Showing generated report now!")
    print(f"\n[!!]View this report anytime at: ~/{reportName}.txt[!!]")
    print("\n" + breakline)
    time.sleep(2)
    os.system(f"cat ~/{reportName}.txt")
    print(breakline)
