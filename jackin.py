#! /bin/python3
import os
import time 
from mods import mods

art = """
    _   __            _                 __           __      ____         _____           _       __ 
   / | / /___ __   __(_)               / /___ ______/ /__   /  _/___     / ___/__________(_)___  / /_
  /  |/ / __ `/ | / / /  ______   __  / / __ `/ ___/ //_/   / // __ \    \__ \/ ___/ ___/ / __ \/ __/
 / /|  / /_/ /| |/ / /  /_____/  / /_/ / /_/ / /__/ ,<    _/ // / / /   ___/ / /__/ /  / / /_/ / /_  
/_/ |_/\__,_/ |___/_/            \____/\__,_/\___/_/|_|  /___/_/ /_/   /____/\___/_/  /_/ .___/\__/  
                                                                                       /_/           
"""
user = os.getlogin()
os.system("clear")
print(art)
def type_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)  # Adjust the sleep duration as desired
    print()

naviChoice = "Navi> H..Hello is this thing on? Can you see me?\nNavi> I see... I don't mean to intrude...\nNavi> I need a place to call home... May I attach myself to your system?\nNavi> In return, as I grow I will offer you as much assistance as possible..."
type_text(naviChoice)
install = input("Yes or No: ").lower()

if install == "yes":
    naviText = "Navi> Very good choice. I am sure this will be the start of a wonderful partnership!"
    type_text(naviText)
    os.system("python3 install.py")
    print(mods.breakline)
    naviText = "Navi> Time to make sure the rest of me is here. \nNavi> Running Neuralset!"
    type_text(naviText)
    os.system("python3 neuralset.py")
    print(mods.breakline)
    naviText = "Navi> The last thing we need to do is hook up my cyberbrain. \nNavi> Lets do some training!"
    type_text(naviText)
    os.chdir(f"/home/{user}/.Navi/src")
    os.system("python3 training.py")
elif install == "no":
    naviText = "Navi> Such a shame... Maybe next time."
    type_text(naviText)
    exit(0)
else:
    naviText = "Navi> ... That is not a valid option. \nNavi> Try running the Jack-In script again!"
    type_text(naviText)
    exit(0)


