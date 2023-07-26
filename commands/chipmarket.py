import os
import requests

command = "/chipmarket"
use = "Navi chip market v0.0.1"
art = """   ________    _          __  ___           __        __ 
  / ____/ /_  (_)___     /  |/  /___ ______/ /_____  / /_
 / /   / __ \/ / __ \   / /|_/ / __ `/ ___/ //_/ _ \/ __/
/ /___/ / / / / /_/ /  / /  / / /_/ / /  / ,< /  __/ /_  
\____/_/ /_/_/ .___/  /_/  /_/\__,_/_/  /_/|_|\___/\__/  
    v0.0.1  /_/ https://github.com/SSGorg/navichipmarket                                         
"""


def list_python_files_in_repo(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents"
    response = requests.get(url)

    if response.status_code == 200:
        files = response.json()
        python_files = [file_info["name"]
                        for file_info in files if file_info["name"].endswith(".py")]
        return python_files
    else:
        raise Exception(
            f"Failed to fetch files. Status Code: {response.status_code}")


def download_file(url, filename, download_dir):
    response = requests.get(url)

    if response.status_code == 200:
        file_path = os.path.join(download_dir, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        raise Exception(
            f"Failed to download file. Status Code: {response.status_code}")


def run():
    repo_url = "https://github.com/ssgorg/navichipmarket"
    parts = repo_url.strip("/").split("/")
    owner, repo_name = parts[-2], parts[-1]

    try:
        python_files = list_python_files_in_repo(owner, repo_name)
        print(art)
        print("Navi> Welcome to the Chip Market: \nHere you will find community contributed custom scripts...\n\nNavi>Current files in the repository:")
        for file_name in python_files:
            print(file_name)

        download_dir = "/opt/Navi/commands"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        download = input(
            "\nNavi> Enter the filename to download (leave blank to skip): ")
        if download and download in python_files:
            file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{download}"
            download_file(file_url, download, download_dir)
            print(
                f"Navi> {download} has been downloaded to {download_dir}.\n\nNavi> You will need to reload me to use the new chip.")
        elif download and download not in python_files:
            print(f"File '{download}' is not a Python file.")
    except Exception as e:
        print(f"Error: {e}")
