#! /bin/python3
import subprocess


def main():
    print("""+===================================================+
Navi Help Menu:
Navi is a simple to use GPT bot that focuses in on assisting with
tasks related to the field of cybersecurity.
[!!] - All commands are preceeded by a '/'
Here is a list of current useable commands:

Command:              Use:
/help                 Displays this text.
/recon                Launches the navi recon automation suite
/clear                Relaunches navi effectively clearing the screen.
/stop                 Stops Navi and returns you to your commandline.
+===================================================+""")
    input("Press enter to continue...")
    subprocess.call(['python3', '.Navi/src/main.py'])

if __name__ == "__main__":
    main()
