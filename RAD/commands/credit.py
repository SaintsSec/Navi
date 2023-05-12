from mods import mods 

command= "/credit"
use= "Shows credit display"
breakline = mods.breakline
def run():
    mods.clearScreen()
    print(mods.art)
    print(f"""NAVI CREDITS:
{breakline}
|Person and or Org    |Contribution                 |
|---------------------|-----------------------------|
|Michael (FoxLab/SSG) |FoxLab VM access / Echo Model|
|---------------------|-----------------------------|
|Mart    (Foxlab/SSG) |Code review / edits          |
|---------------------|-----------------------------|
|Jeremy  (CSI Linux)  |Guidance and implimentation  |
|                     |within CSI Linux.            |
|---------------------|-----------------------------|
|Eric Belardo (Raices)|Giving us a platform to grow |
{breakline}

Thank you all so much for helping make this project a 
reality. Navi is a long time coming for me against all
of the odds. Here we are.. Making it happen. As with 
everything Cybersecurity. Its a Team Sport. 

-Alex
""")
