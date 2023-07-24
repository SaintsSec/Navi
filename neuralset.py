# Imports.
import sys
import subprocess
import errno

# Program.
try:
    print("\nNavi> [!] - Requirements for Debian/Ubuntu:")
    subprocess.run(["sudo", "pip", "install", "-r", "requirements.txt"])
    subprocess.run(["sudo", "pip", "install", "nltk", "speechrecognition", "psutil"])
    subprocess.run(["sudo", "apt-get", "install", "espeak", "espeak-ng", "-y"])
except subprocess.CalledProcessError as e:
    if e.returncode == errno.EPERM:
        sys.exit("You need root permissions to setup the neural files.")
