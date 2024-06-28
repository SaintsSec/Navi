import os
import sys
import requests
import zipfile
import shutil
import subprocess
import uuid

from colorama import Fore
from navi import get_parameters
from navi_shell import print_message, restart_navi

command = "chips"
use = "Manage Navi chips"
aliases = ['chip']


def get_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    response = requests.get(url)

    if response.status_code == 200:
        release = response.json()
        return release
    else:
        return 'No release found'


def search_for_chips(topic, name=None, per_page=10, page=1):
    base_url = "https://api.github.com/search/repositories"
    query = f"topic:{topic}"

    if name:
        query += f"+{name} in:name"

    url = f"{base_url}?q={query}&per_page={per_page}&page={page}"

    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json().get('items', [])
        return repos
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")
        return []


def search(name):
    repos = search_for_chips("navi-chips", name)
    if not repos:
        print(f"{Fore.RED}No Navi Chips found.{Fore.RESET}")
        return
    available_repos = 0
    for repo in repos:
        owner = repo['owner']['login']
        repo_name = repo['name']
        latest_release = get_latest_release(owner, repo_name)['tag_name']
        if latest_release != "No release found":
            available_repos += 1
            print(f"Name: {repo_name}, Owner: {owner} Latest Release: {latest_release}")
    if available_repos == 0:
        print("No Navi Chips found with releases.")


def update_script(download_url, install_path="commands"):
    print("Downloading script...")
    download_guid = str(uuid.uuid4())
    try:
        # Download the latest version
        response = requests.get(download_url)
        zip_path = f"{download_guid}.zip"

        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Unzip the downloaded file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_guid)

        # Copy all files from the extracted archive to the install_path
        extracted_dir = os.path.join(download_guid, os.listdir(download_guid)[0])
        installed_files = []
        for item in os.listdir(extracted_dir):
            s = os.path.join(extracted_dir, item)
            d = os.path.join(install_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
                installed_files.append(d)
            else:
                shutil.copy2(s, d)
                installed_files.append(d)

        # Clean up
        shutil.rmtree(download_guid)
        os.remove(zip_path)

        print("Installing any new packages...")

        # Install new packages from chip-requirements.txt
        requirements_path = os.path.join(install_path, "chip-requirements.txt")
        if os.path.exists(requirements_path):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        os.remove(requirements_path)

        return installed_files

    except Exception as e:
        print(f"An error occurred during the update: {e}")
        return []


def log_installation(repo, installed_files, version):
    log_entry = (
        f"Repo Name: {repo['name']}\n"
        f"Description: {repo['description']}\n"
        f"HTML URL: {repo['html_url']}\n"
        f"Owner: {repo['owner']['login']}\n"
        f"Version: {version}\n"
        f"Installed Files:\n"
    )
    log_entry += "\n".join(installed_files) + "\n\n"

    with open("installed_chips.txt", 'a') as log_file:
        log_file.write(log_entry)


def is_installed(repo_name):
    if not os.path.exists("installed_chips.txt"):
        return False
    with open("installed_chips.txt", 'r') as log_file:
        return repo_name in log_file.read()


def install_chip(name):
    repos = search_for_chips("navi-chips", name)
    if not repos:
        print("No repositories found.")
        return

    repo = repos[0]
    if is_installed(repo['name']):
        print(f"The chip '{repo['name']}' is already installed.")
        return

    release = get_latest_release(repo['owner']['login'], repo['name'])
    if not release:
        print("No release found for this repository.")
        return

    download_url = release['zipball_url']
    version = release['tag_name']
    installed_files = update_script(download_url)

    log_installation(repo, installed_files, version)
    print(f"Chip '{repo['name']}' installed successfully. Restarting Navi...")
    restart_navi()


def uninstall_chip(name):
    install_path = "commands"

    # Check if the chip is installed by reading the log file
    if not os.path.exists("installed_chips.txt"):
        print(f"{Fore.RED}No chips installed.{Fore.RESET}")
        return

    # Read the installed chip log
    with open("installed_chips.txt", 'r') as log_file:
        lines = log_file.readlines()

    # Find the chip entry in the log
    package_start = None
    for i, line in enumerate(lines):
        if line.strip() == f"Repo Name: {name}":
            package_start = i
            break

    if package_start is None:
        print(f"The chip '{name}' is not installed.")
        return

    # Find the end of the chip entry in the log
    package_end = package_start
    while package_end < len(lines) and lines[package_end].strip() != "":
        package_end += 1

    # Extract the installed files from the log
    installed_files = []
    for line in lines[package_start:package_end]:
        if line.startswith("Installed Files:"):
            continue
        installed_files.append(line.strip())

    # Delete the installed files
    for file_path in installed_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

    # Remove the chip entry from the log
    new_lines = lines[:package_start] + lines[package_end:]
    with open("installed_chips.txt", 'w') as log_file:
        log_file.writelines(new_lines)

    print(f"{Fore.GREEN}The chip {Fore.WHITE}'{name}' {Fore.GREEN}has been uninstalled successfully.{Fore.RESET}")
    restart_navi()


def list_installed_chips():
    log_file_path = "installed_chips.txt"

    if not os.path.exists(log_file_path):
        print("No chips are installed.")
        return

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    if not lines:
        print("No chips are installed.")
        return

    modules = []
    module_info = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Repo Name:"):
            module_name = line.split("Repo Name: ")[1]
            description = lines[i+1].split("Description: ")[1].strip()
            html_url = lines[i+2].split("HTML URL: ")[1].strip()
            owner = lines[i+3].split("Owner: ")[1].strip()
            version = lines[i+4].split("Version: ")[1].strip()

            module_info = {
                "name": module_name,
                "description": description,
                "html_url": html_url,
                "owner": owner,
                "version": version
            }
            modules.append(module_info)
        i += 1

    if modules:
        print("Installed Chips:")
        for module in modules:
            print(f"- {module['name']} (Owner: {module['owner']}, Version: {module['version']})")
    else:
        print("No chips are installed.")


def about_chip(name):
    log_file_path = "installed_chips.txt"

    if not os.path.exists(log_file_path):
        print("No chips are installed.")
        return None

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    if not lines:
        print("No chips are installed.")
        return None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Repo Name:") and line.split("Repo Name: ")[1] == name:
            module_name = line.split("Repo Name: ")[1]
            description = lines[i+1].split("Description: ")[1].strip()
            html_url = lines[i+2].split("HTML URL: ")[1].strip()
            owner = lines[i+3].split("Owner: ")[1].strip()
            version = lines[i+4].split("Version: ")[1].strip()
            installed_files = []

            j = i + 5
            while j < len(lines) and lines[j].strip() != "":
                installed_files.append(lines[j].strip())
                j += 1

            # Check for the latest version
            latest_release = get_latest_release(owner, module_name)
            if latest_release:
                latest_version = latest_release['tag_name']
                if latest_version != version:
                    print(f"{Fore.GREEN}A later version is available: {latest_version}.{Fore.RESET} To update type {Fore.YELLOW}'chips update {name}'{Fore.RESET}")
                else:
                    print("You have the latest version installed.")
            else:
                latest_version = "Unknown"

            module_info = {
                "name": module_name,
                "description": description,
                "html_url": html_url,
                "owner": owner,
                "version": version,
                "installed_files": installed_files,
                "latest_version": latest_version
            }
            return module_info
        i += 1

    print(f"The chip '{name}' is not installed.")
    return None


def remove_old_log_entry(chip_name):
    log_file_path = "installed_chips.txt"

    if not os.path.exists(log_file_path):
        return

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if line.startswith("Repo Name:") and line.split("Repo Name: ")[1].strip() == chip_name:
            skip = True
        if skip and line.strip() == "":
            skip = False
            continue
        if not skip:
            new_lines.append(line)

    with open(log_file_path, 'w') as log_file:
        log_file.writelines(new_lines)


def update_chip(chip_name):
    chip_info = about_chip(chip_name)
    if not chip_info:
        print(f"The chip '{chip_name}' is not installed.")
        return

    if chip_info['latest_version'] != chip_info['version']:
        print(f"Updating chip '{chip_name}' to version {chip_info['latest_version']}...")
        release = get_latest_release(chip_info['owner'], chip_info['name'])
        if not release:
            print(f"Failed to get the latest release for {chip_name}.")
            return

        download_url = release['zipball_url']
        installed_files = update_script(download_url)

        # Remove the old log entry
        remove_old_log_entry(chip_name)

        # Log the new installation
        repo = {
            'name': chip_info['name'],
            'description': chip_info['description'],
            'html_url': chip_info['html_url'],
            'owner': {'login': chip_info['owner']}
        }
        log_installation(repo, installed_files, chip_info['latest_version'])
        print(f"Chip '{chip_name}' updated successfully. Restarting Navi...")
        restart_navi()


def help_text():
    print_message("Chip Manager\n"
                  "chips [install | uninstall | search | update] [app/query]\n\n"
                  "List currently installed chips\n"
                  "chips list")


def run(arguments=None):
    argv = get_parameters(arguments.text)
    argv.pop(0)

    if not argv:
        help_text()
        return

    command = argv[0]

    if command == "list":
        list_installed_chips()
        return
    if len(argv) == 1:
        chip_info = about_chip(argv[0])
        if chip_info:
            print(f"Name: {chip_info['name']}")
            print(f"Description: {chip_info['description']}")
            print(f"URL: {chip_info['html_url']}")
            print(f"Owner: {chip_info['owner']}")
            print(f"Your Version: {chip_info['version']}")
            print(f"Latest Version: {chip_info['latest_version']}")
        return

    if command == "install" and len(argv) > 1:
        install_chip(argv[1])
        return

    if command == "uninstall" and len(argv) > 1:
        uninstall_chip(argv[1])
        return

    if command == "update" and len(argv) > 1:
        update_chip(argv[1])
        return

    if command == "search" and len(argv) > 1:
        search(argv[1])
        return

    help_text()
