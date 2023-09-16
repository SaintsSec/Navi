import os

breakline = "+===================================================+"

versionNum = "0.1.2"


# The cover art:
art = f"""{breakline}
|               _   __            _                 |
|              / | / /___ __   __(_)                |
|             /  |/ / __ `/ | / / /                 |
|            / /|  / /_/ /| |/ / /                  |
|           /_/ |_/\__,_/ |___/_/ v{versionNum}            |
|     Type 'run' for chips or '/stop' to exit       |
|    Otherwise type a prompt to talk to the AI      |
{breakline}
"""
vbusterArt = f"""{breakline}
|         _    ______             __                |           
|        | |  / / __ )__  _______/ /____  _____     |
|        | | / / __  / / / / ___/ __/ _ \/ ___/     |
|        | |/ / /_/ / /_/ (__  ) /_/  __/ /         |
|        |___/_____/\__,_/____/\__/\___/_/          |
|                Powered by ClamAV                  |
{breakline}

"""
reconArt = f"""{breakline}
|         ____                                      |                     
|        / __ \___  _________  ____                 |
|       / /_/ / _ \/ ___/ __ \/ __ \\                |
|      / _, _/  __/ /__/ /_/ / / / /                |
|     /_/ |_|\___/\___/\____/_/ /_/                 |                                
{breakline}
"""
gptArt = f"""{breakline}
|     _   __            _       __________  ______  |
|    / | / /___ __   __(_)     / ____/ __ \/_  __/  |
|   /  |/ / __ `/ | / / /_____/ / __/ /_/ / / /     | 
|  / /|  / /_/ /| |/ / /_____/ /_/ / ____/ / /      |
| /_/ |_/\__,_/ |___/_/      \____/_/     /_/       |
|                                                   |
{breakline}
"""

helpArt = f"""{breakline}
      _   __            _    __  __     __    
     / | / /___ __   __(_)  / / / /__  / /___ 
    /  |/ / __ `/ | / / /  / /_/ / _ \/ / __ \\
   / /|  / /_/ /| |/ / /  / __  /  __/ / /_/ /
  /_/ |_/\__,_/ |___/_/  /_/ /_/\___/_/ .___/ 
                                     /_/      
{breakline}
"""
# Clear Screen Code


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Nmap Commands
nMapCommands = """Before you pick your options here are some nmap example's to work with.
1. nmap -sV (service version detection) IpAddress/URLHere
2. nmap -sS (TCP SYN scan) IpAddress/URLHere
3. nmap --top-ports (scan top ports) IpAddress/URLHere
4. nmap -O (operating system detection) IpAddress/URLHere
5. nmap -A (aggressive scan) IpAddress/URLHere

Navi> [\u2713] - for example you can chain these: nmap -sSV IpAddress/URLHere 
"""
