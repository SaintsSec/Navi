import subprocess

install = ["pip", "install", "-r", "requirements.txt"]
subprocess.run(install)

import nltk

nltk.download('punkt')
nltk.download('wordnet')

print("[!] REQUIREMENTS INSTALLED")
