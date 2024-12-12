import subprocess
import os
import sys
from getpass import getpass
import tempfile
import shutil

from IPython.core.debugger import prompt

password = getpass("Enter your sudo password: ")

def intro_text():
    print("Welcome to the Navi3b model installer.\n============\nThis script will install Ollama and the Navi3b model.\n"
          "It is recommended to have a stable internet connection for this process. \nIf you have any questions, please refer to the Navi documentation."
          "\nIt should also be noted that this is a local AI model\nExpect it to be slower than its larger server based counterpart.")

def install_ollama():
    try:
        process = subprocess.run(
            ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Ollama was installed successfully!")
        print("stdout:", process.stdout)
        print("stderr:", process.stderr)
    except subprocess.CalledProcessError as e:
        print("Ollama installation failed!")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)

def check_ollama():
    try:
        process = subprocess.run(
            ["ollama", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Ollama is already installed!")
        print("stdout:", process.stdout)
        print("stderr:", process.stderr)
    except subprocess.CalledProcessError as e:
        print("ollama is not installed!")
        ollama_choice = input("Would you like to install Ollama now? \nOptions: (Y)es, (N)o\nUser Input > ").strip().lower()
        if ollama_choice in ["yes", "y"]:
            install_ollama()
        else:
            print("Understood, exiting now.")
            sys.exit(0)
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)

def install_navi3b():
    with tempfile.NamedTemporaryFile("w", delete=False) as temp_script:
        temp_script.write(f"#!/bin/bash\necho {password}\n")
        temp_script_path = temp_script.name

    os.chmod(temp_script_path, 0o700)

    env = os.environ.copy()
    env["SUDO_ASKPASS"] = temp_script_path
    try:
        process = subprocess.run(
            ["git", "clone", "https://github.com/saintssec/navi3b"],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        print("Command succeeded!")
        print("stdout:", process.stdout)
        print("stderr:", process.stderr)
    except subprocess.CalledProcessError as e:
        print("Command failed!")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)

    try:
        process = subprocess.run(
            ["sudo", "ollama", "create", "navi-cli", "-f", "./navi3b/navi3b.modelfile"],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        print("Command succeeded!")
        print("stdout:", process.stdout)
        print("stderr:", process.stderr)
    except subprocess.CalledProcessError as e:
        print("Command failed!")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
    finally:
        os.remove(temp_script_path)
        shutil.rmtree("./navi3b")

def main():
    intro_text()
    user_input = input("============\nWould you like to install the Navi3b system? \nOptions: (Y)es, (N)o\nUser Input > ").strip().lower()
    if user_input in ["yes", "y"]:
        check_ollama()
        install_navi3b()
    else:
        print("Understood exiting now")
        sys.exit(0)

if __name__ == "__main__":
    main()