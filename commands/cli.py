import os

command = "/cli"
use = "Navi commandline passthrough"

def run():
    command = input("Enter a linux command: ")
    os.system(f"{command}")
