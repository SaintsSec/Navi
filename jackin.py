#! /bin/python3
import os
import getpass
from mods import mods
from mods import typewriter
art = """
    _   __            _                 __           __      ____         _____           _       __ 
   / | / /___ __   __(_)               / /___ ______/ /__   /  _/___     / ___/__________(_)___  / /_
  /  |/ / __ `/ | / / /  ______   __  / / __ `/ ___/ //_/   / // __ \    \__ \/ ___/ ___/ / __ \/ __/
 / /|  / /_/ /| |/ / /  /_____/  / /_/ / /_/ / /__/ ,<    _/ // / / /   ___/ / /__/ /  / / /_/ / /_  
/_/ |_/\__,_/ |___/_/            \____/\__,_/\___/_/|_|  /___/_/ /_/   /____/\___/_/  /_/ .___/\__/  
                                                                                       /_/           
"""
user = getpass.getuser()
os.system("clear")
print(art)
type_text = typewriter.typewriter

naviChoice = "Navi> H..Hello is this thing on? Can you see me?\nNavi> I see... I don't mean to intrude...\nNavi> I need a place to call home... May I attach myself to your system?\nNavi> In return, as I grow I will offer you as much assistance as possible..."
type_text(naviChoice)
install = input("\nYes or No: ").lower()

if install == "yes":
    print(mods.breakline)
    naviText = "Navi> Time to make sure the rest of my requirements are installed.. \nNavi> Running Neuralset!"
    type_text(naviText)
    os.system("python3 neuralset.py")
    print(mods.breakline)
    naviText = "Navi> The next thing we need to do is hook up my cyberbrain. \nNavi> Lets do some training!"
    type_text(naviText)
    os.chdir("src/")
    os.system("python3 training.py")
    print(mods.breakline)
    naviText = "Navi> Let clean all of this up and finish the setup."
    type_text(naviText)
    os.chdir("..")
    os.system("python3 install.py")
    naviText = "Navi> Looks like we are finished here.. \nNavi> I will be here if you need me. Just open a terminal and type 'navi'."
elif install == "no":
    naviText = "Navi> Such a shame... Maybe next time."
    type_text(naviText)
    exit(0)
else:
    naviText = "Navi> ... That is not a valid option. \nNavi> Try running the Jack-In script again!"
    type_text(naviText)
    exit(0)
