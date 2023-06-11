#!/bin/python3

#TODO - Add rkhunter

#imports
import os
from mods import mods
import commands

command = "/vbuster"
use = "Virus removal suite"

#global variables
breakline = mods.breakline
art = mods.vbusterArt

def run():
    print(art)
    #Setup
    scanOptions = input("Navi> [!] - What options do you want to scan with (ex: -r): ")
    scanDir = input("Navi> [!] - Where do you want to scan (ex: ~/): ")
    print("Navi> [!] - Starting scan now... Just a sec.")
    #Start
    os.system(f"clamscan {scanOptions} {scanDir}")
    #TODO - Add ability to save results to a .txt (maybe PDF later).
    print("\n" + breakline + "\n")