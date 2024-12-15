import subprocess
import os
import sys
import tempfile
import shutil
from getpass import getpass
from typing import Tuple


def intro_text():
    print("Welcome to the Navi3b model installer.\n============\nThis script will install Ollama and the Navi3b model.\n"
          "It is recommended to have a stable internet connection for this process. \nIf you have any questions, please refer to the Navi documentation."
          "\nIt should also be noted that this is a local AI model\nExpect it to be slower than its larger server based counterpart.")


def install_ollama() -> bool:
    import platform
    try:
        if platform.system() in ["Linux", "Darwin"]:  # macOS/Linux
            print("Installing Ollama on macOS/Linux...")
            subprocess.run(
                ["curl", "-fsSL", "https://ollama.com/install.sh", "|", "sh"],
                shell=True,  # Use shell to handle the pipe
                check=True,
                capture_output=True,
                text=True,
            )
        elif platform.system() == "Windows":
            print("Installing Ollama on Windows...")
            # Assuming Windows uses an executable installer
            subprocess.run(
                ["powershell", "-Command",
                 "Invoke-WebRequest -Uri https://ollama.com/install.exe -OutFile ollama_installer.exe; Start-Process -FilePath ./ollama_installer.exe -Wait"],
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
        else:
            print("Unsupported platform for Ollama installation.")
            return False

        print("Ollama installation succeeded!")
        return True
    except subprocess.CalledProcessError as e:
        print("Ollama installation failed!")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        return False


def ollama_installed() -> bool:
    try:
        subprocess.run(
                ["ollama", "--version"],
                check=True,
                capture_output=True,
                text=True,
            )
        return True
    except subprocess.CalledProcessError as e:
        return False


def is_ollama_service_running() -> bool:
    """
    Checks if the 'ollama' service is running by executing 'ollama --version'.
    If the service is not running, it outputs a warning.
    """
    try:
        # Run `ollama --version` to check the service status
        process = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        # If no warning is present, the service is running
        if "Warning: could not connect to a running Ollama instance" in process.stderr:
            return False
        return True
    except subprocess.CalledProcessError as e:
        print("Error running 'ollama --version':", e.stderr)
        return False

def start_ollama_service():
    try:
        subprocess.run(
            ["ollama", "serve"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print("Ollama service already running.")

def check_and_start_ollama_service():
    """
    Ensures the 'ollama' service is running. Starts it if it's not running.
    """
    if is_ollama_service_running():
        print("Ollama service is already running.")
    else:
        print("Ollama service is not running. Attempting to start it...")
        start_ollama_service()

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

def check_model_installed() -> Tuple[bool, bool]:
    try:
        # Run the command to check if the model exists
        process = subprocess.run(
            ["ollama", "show", "navi-cli"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True, False  # Model is installed, no unexpected error
    except subprocess.CalledProcessError as e:
        if "Error: model 'navi-cli' not found" in e.stderr:
            return False, False  # Model not installed, no unexpected error
        else:
            print("An unexpected error occurred.")
            print("stderr:", e.stderr)
            return False, True  # Model not installed, unexpected error


def install_model():
    import platform
    is_windows = platform.system() == "Windows"
    temp_script_path = None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.join(script_dir, "navi3b")
    os.mkdir(repo_dir)

    #create dir for git clone
    # then clean it after

    if not is_windows:
        # Get sudo password for macOS/Linux
        password = getpass("Enter your sudo password: ")

        # Create a temporary sudo-askpass script
        with tempfile.NamedTemporaryFile("w", delete=False) as temp_script:
            temp_script.write(f"#!/bin/bash\necho {password}\n")
            temp_script_path = temp_script.name
        os.chmod(temp_script_path, 0o700)

    try:
        # Clone the GitHub repository
        print("Cloning model from github.com/saintssec/navi3b...")
        subprocess.run(
            ["git", "clone", "https://github.com/saintssec/navi3b", repo_dir],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Git clone succeeded!")
    except subprocess.CalledProcessError as e:
        print("Git clone failed!")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        if temp_script_path:
            os.remove(temp_script_path)
        return

    print("Verifying model...")
    model_file_path = os.path.join(repo_dir, "navi3b.modelfile")
    if not os.path.exists(model_file_path):
        print(f"Error: {model_file_path} not found.")
        if temp_script_path:
            os.remove(temp_script_path)
        return
    # Create the model using Ollama
    try:
        print("Creating model... this may take a while...")
        if is_windows:
            # On Windows, no sudo is needed
            subprocess.run(
                ["ollama", "create", "navi-cli", "-f", model_file_path],
                check=True,
                capture_output=True,
                text=True,
            )
        else:
            # On macOS/Linux, use sudo with the sudo-askpass script
            env = os.environ.copy()
            env["SUDO_ASKPASS"] = temp_script_path
            subprocess.run(
                ["sudo", "ollama", "create", "navi-cli", "-f", model_file_path],
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )

        print("Model creation succeeded!")
    except subprocess.CalledProcessError as e:
        print("Model creation failed!")
        print("Return code:", e.returncode)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
    finally:
        # Cleanup: Remove the temporary script and cloned directory
        if temp_script_path:
            os.remove(temp_script_path)
        shutil.rmtree("./navi3b", ignore_errors=True)

def main():
    intro_text()
    user_input = input("============\nWould you like to install the Navi3b system? \nOptions: (Y)es, (N)o\nUser Input > ").strip().lower()
    if user_input in ["yes", "y"]:
        check_ollama()
        install_model()
    else:
        print("Understood exiting now")
        sys.exit(0)

if __name__ == "__main__":
    main()