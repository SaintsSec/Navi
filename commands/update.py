import os
import sys
import requests

command = "/update"
use = "Updates navi"
ai_name_rep = "Navi>"


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
                'sudo cp -r /opt/Navi/var/ /tmp/Navi_Update',
                'sudo cp -r /opt/Navi/src /tmp/Navi_Update',
                'mkdir /tmp/Navi',
                'git clone https://github.com/SSGOrg/Navi /tmp/Navi',
                'sudo rm -rf /opt/Navi',
                'sudo mkdir /opt/Navi',
                'sudo cp -r /tmp/Navi /opt/',
                'sudo cp desktop/navi.desktop /usr/share/applications/navi.desktop',
                'sudo rm -rf /opt/Navi/.git/',
                'sudo rm -rf /opt/Navi/.github/',
                'sudo rm /opt/Navi/README.md',
                'sudo rm /opt/Navi/CONTRIBUTING.md',
                'sudo rm /opt/Navi/CODE_OF_CONDUCT.md',
                'sudo rm /opt/Navi/install.py',
                'sudo rm /opt/Navi/csi-jackin.py',
                'sudo rm /opt/Navi/csi-install.py',
                'sudo rm /opt/Navi/neuralset.py',
                'sudo rm /opt/Navi/requirements.txt',
                'sudo rm /opt/Navi/jackin.py',
                'sudo rm -rf /opt/Navi/var && sudo mv /tmp/Navi_Update/var /opt/Navi',
                'sudo rm -rf /opt/Navi/src && sudo mv /tmp/Navi_Update/src /opt/Navi',
                'sudo chmod -R 777 /opt/Navi',

            ]

            # Shell related commands
            # commands += [handle_shell()]

            # Run the commands
            for c in commands:
                if len(c) <= 0:
                    continue
                os.system(c)
            
                print(f"{ai_name_rep} [!!] - Update complete, to see changes you will need to restart me.")
                exit(0)

            if updateChoice == "no":
                return f"{ai_name_rep} You really should consider updating."

    else:
        return f"{ai_name_rep} - [!!] You are running the latest version!"


def checkVersion():
    current_version = "0.1.1"  # Replace with your actual current version
    repo_owner = "SSGOrg"  # Replace with the actual owner name
    repo_name = "Navi"  # Replace with the actual repository name

    result = check_for_new_release(current_version, repo_owner, repo_name)
    print(result)


def run():
    checkVersion()
