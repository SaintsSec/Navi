import os

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

# Line Break
breakline = "+===================================================+ "

# Clear Screen Code
clearScreen = os.system('cls' if os.name == 'nt' else 'clear')


