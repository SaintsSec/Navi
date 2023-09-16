import os
import shutil
import subprocess

art = """
    _   __            _                 __           __      ____         _____           _       __ 
   / | / /___ __   __(_)               / /___ ______/ /__   /  _/___     / ___/__________(_)___  / /_
  /  |/ / __ `/ | / / /  ______   __  / / __ `/ ___/ //_/   / // __ \    \__ \/ ___/ ___/ / __ \/ __/
 / /|  / /_/ /| |/ / /  /_____/  / /_/ / /_/ / /__/ ,<    _/ // / / /   ___/ / /__/ /  / / /_/ / /_  
/_/ |_/\__,_/ |___/_/            \____/\__,_/\___/_/|_|  /___/_/ /_/   /____/\___/_/  /_/ .___/\__/  
                                                                                       /_/           
"""


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def is_root():
    """Check if the script has root privileges."""
    return os.geteuid() == 0


def install_pip(distribution):
    """Install pip based on the given Linux distribution."""
    install_commands = {
        "ubuntu": ["sudo", "apt-get", "install", "python3-pip", "-y"],
        "debian": ["sudo", "apt-get", "install", "python3-pip", "-y"],
        "fedora": ["sudo", "dnf", "install", "python3-pip", "-y"],
        "centos": ["sudo", "yum", "install", "python3-pip", "-y"],
        # Add other distributions as needed
    }

    command = install_commands.get(distribution.lower())

    if command:
        subprocess.run(command)
    else:
        print("Sorry, this distribution is not supported yet.")
        exit(1)


def install_requirements():
    """Install the requirements using pip."""
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])


def setup_aliases(shell_choice):
    """Set up two aliases in the given shell's configuration file."""
    config_files = {
        "bash": "~/.bashrc",
        "zsh": "~/.zshrc"
    }

    config_path = os.path.expanduser(
        config_files.get(shell_choice, "~/.bashrc"))

    aliases = {
        "navishell": "cd /opt/Navi/ && python3 /opt/Navi/navi-shell.py && cd",
        "naviweb": "python3 /opt/Navi/navi-web.py"
    }

    # Check for existing aliases
    with open(config_path, 'r') as file:
        config_contents = file.read()

        # Create a list of existing aliases to remove
        aliases_to_remove = []

        for alias_name in aliases.keys():
            if f"alias {alias_name}=" in config_contents:
                print(f"Alias '{alias_name}' already exists.")
                aliases_to_remove.append(alias_name)

        # Remove the existing aliases from the dictionary
        for alias_name in aliases_to_remove:
            del aliases[alias_name]

    # Add new aliases
    with open(config_path, 'a') as file:
        for alias_name, command in aliases.items():
            file.write(f"\nalias {alias_name}='{command}'\n")
            print(f"Alias '{alias_name}' added.")

    print(
        f"You may need to source {config_path} or restart your terminal/shell.")


def delete_navi():
    # Remove /opt/Navi if it exists
    if os.path.exists("/opt/Navi"):
        print("Removing existing /opt/Navi directory...")
        shutil.rmtree("/opt/Navi")


def copy_navi():
    # Copy the Navi directory to /opt
    print("Copying Navi to /opt...")
    shutil.copytree(".", "/opt/Navi")


def cleanup_install_directory(files_to_remove):
    """Remove specific files and directories after installation."""
    os.chdir('/opt/Navi')
    for file_or_dir in files_to_remove:
        path_to_remove = os.path.join(".", file_or_dir)
        if os.path.exists(path_to_remove):
            if os.path.isdir(path_to_remove):
                shutil.rmtree(path_to_remove)
            else:
                os.remove(path_to_remove)
    print("Cleaned up installation directory.")


def setup_service(service_file_path="./rasa-core.service"):
    """Set up the Rasa core service."""
    dest_path = "/etc/systemd/system/"

    # Copy the service file
    shutil.copy2(service_file_path, dest_path)
    print(f"Service file copied to {dest_path}")

    # Enable the service
    subprocess.run(["systemctl", "enable", "rasa-core.service"])
    print("rasa-core.service enabled.")


def set_permissions_recursive(directory_path, permission=0o777):
    """Recursively set permissions for a directory and all its contents."""
    for dirpath, dirnames, filenames in os.walk(directory_path):
        os.chmod(dirpath, permission)
        for filename in filenames:
            os.chmod(os.path.join(dirpath, filename), permission)


if __name__ == "__main__":
    # Check for root privileges
    if not is_root():
        print("Please run this script with sudo privileges.")
        exit(1)
    clear_screen()
    print(art)

    # Choose Distribution
    print("Choose your Linux distribution:")
    print("1. Ubuntu/Debian")
    print("2. Fedora")
    print("3. CentOS")
    # Extend with other distributions as needed

    choice = input("Enter the number corresponding to your distribution: ")

    distros = {
        "1": "ubuntu",
        "2": "fedora",
        "3": "centos",
        # Extend with other distributions as needed
    }

    distribution = distros.get(choice)

    if not distribution:
        print("Invalid choice!")
        exit(1)

    # Choose Shell
    print("\nChoose your shell:")
    print("1. bash")
    print("2. zsh")

    shell_choice = input("Enter the number corresponding to your shell: ")

    shells = {
        "1": "bash",
        "2": "zsh"
    }

    shell = shells.get(shell_choice)

    if not shell:
        print("Invalid shell choice!")
        exit(1)

     # List of files/directories to remove after installation
    files_to_delete = ["jackin.py", "requirements.txt",
                       "rasa-core.service", "README.md", ".git", ".gitignore"]
    # Install requirements and set up aliases
    delete_navi()
    copy_navi()
    install_pip(distribution)
    install_requirements()
    setup_aliases(shell)
    setup_service()
    cleanup_install_directory(files_to_delete)
    set_permissions_recursive("/opt/Navi")
