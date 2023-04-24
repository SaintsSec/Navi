import os

breakline = "+===================================================+"

# The cover art:
art = f"""{breakline}
|       _   __            _    __________  ______   |
|      / | / /___ __   __(_)  / ____/ __ \/_  __/   |
|     /  |/ / __ `/ | / / /  / / __/ /_/ / / /      |
|    / /|  / /_/ /| |/ / /  / /_/ / ____/ / /       |
|   /_/ |_/\__,_/ |___/_/   \____/_/v0.2 /_/        |
|    Type "/help" for help menu "/stop" to exit     |
{breakline}
"""

# Clear Screen Code
def clearScreen():
  os.system('cls' if os.name == 'nt' else 'clear')

## Nmap Commands
nMapCommands = """Before you pick your options here are some nmap example's to work with.
1. nmap -sV (service version detection) IpAddress/URLHere
2. nmap -sS (TCP SYN scan) IpAddress/URLHere
3. nmap --top-ports (scan top ports) IpAddress/URLHere
4. nmap -O (operating system detection) IpAddress/URLHere
5. nmap -A (aggressive scan) IpAddress/URLHere

Navi> [\u2713] - for example you can chain these: nmap -sSVAO IpAddress/URLHere 
"""
