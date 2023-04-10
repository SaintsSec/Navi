#! /bin/python3
import os, subprocess, time
from mods import mods

breakline = mods.breakline

def main():
    #Nmap Setup
    scanIP = input("Navi> Give me an IP to scan: ")
    scanOptions = input("Navi> What type of scan (ex: -sV): ")
    reportName = input("Navi> What would you like to name the report(ex: Report1): ")
    print(breakline + "\n\n")

    #Scan execution
    print("The Process:")
    print(f"[\u2713] - Starting Scan now: nmap {scanOptions} {scanIP}")
    os.system(f"nmap {scanOptions} {scanIP} > ~/{reportName}.txt")
    print("[\u2713] - Scan complete!!")
    print(f"[\u2713] - Showing generated report now! \nScan can be viwed anytime at: ~/{reportName}.txt")

    #Show nmap report
    print("\n\n" + breakline)
    os.system(f"cat ~/{reportName}.txt")
    print(breakline)
    input("Press enter to continue: ")
    subprocess.call(['python3', './main.py'])

if __name__ == "__main__":
    main()
