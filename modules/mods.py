import os

banner = '''+============================================+
|--------------------------------------------|
|              _   __            _           |
|             / | / /___ __   __(_)          |
|            /  |/ / __ `/ | / / /           |
|           / /|  / /_/ /| |/ / /            |
|          /_/ |_/\__,_/ |___/_/             |
|              Version:0.0.1                 |
|--------------------------------------------|
|           SSG Command & Control            |
|      Type 'help' to bring up commands      |
+============================================+'''

bothelp = """+============================================+
| Basic Usage:                               |
| To use the AI simply start chatting        |
| it will respond as best it can.            |
+--------------------------------------------|
| Found an problem or want to contribute?    |
| https://github.com/SSGorg/Navi             |
+ -------------------------------------------+
| Commands:                                  |
| cryptex - Shows Cryptex Menu if installed  |
| cls     - Clears the screen                |
| exit    - exits the current session        |
+============================================+"""

def clear():
    if(os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')


