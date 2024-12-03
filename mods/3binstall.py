import subprocess
import os
import sys

def intro_text():
    print("Welcome to the Navi3b model installer.\n============\nThis script will install Ollama and the Navi3b model.\n"
          "It is recommended to have a stable internet connection for this process. \nIf you have any questions, please refer to the Navi documentation."
          "\nIt should also be noted that this is a local AI model\nExpect it to be slower than its larger server based counterpart.")

def install_navi3b():
    print("Installing navi3b model...")
    try:
        if os.path.exists("navi3b"):
            print("navi3b directory already exists, skipping clone.")
            subprocess.run(["bash", "-s", "navi3b/install.sh"], check=True)
        else:
            subprocess.run(["git", "clone", "https://github.com/saintssec/navi3b"], check=True)
            subprocess.run(["bash", "-s", "navi3b/install.sh"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install navi3b model: {e}")

def main():
    intro_text()
    user_input = input("============\nWould you like to install the Navi3b system? \nOptions: (Y)es, (N)o\nUser Input > ").strip().lower()
    if user_input in ["yes", "y"]:
        install_navi3b()
    else:
        print("Understood exiting now")
        sys.exit(0)

if __name__ == "__main__":
    main()