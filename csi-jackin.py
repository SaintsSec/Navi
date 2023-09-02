#! /bin/python3
import os
import getpass
from mods import mods
from mods import typewriter
art = """
   ___________ ____                __           __   _          _____           _       __ 
  / ____/ ___//  _/               / /___ ______/ /__(_)___     / ___/__________(_)___  / /_
 / /    \__ \ / /   ______   __  / / __ `/ ___/ //_/ / __ \    \__ \/ ___/ ___/ / __ \/ __/
/ /___ ___/ // /   /_____/  / /_/ / /_/ / /__/ ,< / / / / /   ___/ / /__/ /  / / /_/ / /_  
\____//____/___/            \____/\__,_/\___/_/|_/_/_/ /_/   /____/\___/_/  /_/ .___/\__/  
                                                                             /_/           
"""
os.system("clear")
print(art)

os.system("python3 neuralset.py")
os.chdir("src/")
os.system("python3 csi-training.py")
os.chdir("..")
os.system("python3 csi-install.py")
