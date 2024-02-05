import os
import requests
import pyfiglet
import click 

command = "/update"
use = "Updates navi"
ai_name_rep = "Navi>"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def headerArt():
    header = pyfiglet.figlet_format("Navi Updates", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))

def get_latest_release(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        tag_name = data.get('tag_name')
        release_name = data.get('name')
        html_url = data.get('html_url')

        return {
            'tag_name': tag_name,
            'release_name': release_name,
            'html_url': html_url
        }
    else:
        return None


def is_new_release(current_version, latest_version):
    return current_version < latest_version


def check_for_new_release(current_version, repo_owner, repo_name):
    latest_release = get_latest_release(repo_owner, repo_name)

    if latest_release and is_new_release(current_version, latest_release['tag_name']):
        print(
            f"{ai_name_rep} - [!!] New release available!!\n{latest_release['release_name']} ({latest_release['tag_name']})\nURL: {latest_release['html_url']}")
        updateChoice = input(
            f"\n{ai_name_rep} Would you like to update now\n(yes / no): ").lower()
        if updateChoice == "yes":
            # List over commands to run
            os.chdir("/tmp/")
            commands = []

            # Navi related commands
            commands += [
                'sudo rm -rf /tmp/Navi_Update',
                'sudo rm -rf /tmp/Navi',
                'mkdir /tmp/Navi_Update',
                'mkdir /tmp/Navi',
                'git clone https://github.com/SaintsSec/Navi /tmp/Navi',
                'sudo rm -rf /opt/Navi',
                'sudo mkdir /opt/Navi',
                'sudo cp -r /tmp/Navi /opt/',
                'sudo rm -rf /opt/Navi/.git/',
                'sudo rm -rf /opt/Navi/.github/',
                'sudo rm /opt/Navi/README.md',
                'sudo rm /opt/Navi/CONTRIBUTING.md',
                'sudo rm /opt/Navi/CODE_OF_CONDUCT.md',
                'sudo rm -rf /tmp/Navi_Update',
                'sudo rm -rf /tmp/Navi',
                'sudo chmod -R 777 /opt/Navi',
            ]

            # Shell related commands
            # commands += [handle_shell()]

            # Run the commands
            for c in commands:
                if len(c) <= 0:
                    continue
                os.system(c)
            print(
                f"\n\n{ai_name_rep} Update complete, type 'navi' in the CLI for update to take effect!")
            exit(0)

        if updateChoice == "no":
            return f"{ai_name_rep} You really should consider updating."

    else:
        return f"{ai_name_rep} - [!!] You are running the latest version!"


def checkVersion():
    current_version = "0.1.3"  # Replace with your actual current version
    repo_owner = "SaintsSec"  # Replace with the actual owner name
    repo_name = "Navi"  # Replace with the actual repository name

    result = check_for_new_release(current_version, repo_owner, repo_name)
    print(result)


def run():
    clear_screen()
    headerArt()
    checkVersion()
