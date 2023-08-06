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
os.system("clear")
print(art)

os.system("python3 neuralset.py")
os.chdir("src/")
os.system("python3 csi-training.py")
os.chdir("..")
os.system("python3 csi-install.py")
