import os
import requests

command = "/chipmarket"
use = "Navi chip market v0.0.2"
art = """   ________    _          __  ___           __        __ 
  / ____/ /_  (_)___     /  |/  /___ ______/ /_____  / /_
 / /   / __ \/ / __ \   / /|_/ / __ `/ ___/ //_/ _ \/ __/
/ /___/ / / / / /_/ /  / /  / / /_/ / /  / ,< /  __/ /_  
\____/_/ /_/_/ .___/  /_/  /_/\__,_/_/  /_/|_|\___/\__/  
    v0.0.1  /_/ https://github.com/SSGorg/navichipmarket                                         
"""

# Replace with the GitHub repository URL
REPO_URL = "https://github.com/SSGorg/navichipmarket"
# Replace with the directory for Python files
PYTHON_DOWNLOAD_DIR = "/opt/Navi/commands"
# Replace with the directory for JSON files
JSON_DOWNLOAD_DIR = "/opt/Navi/src/intenses_db"


def list_files_in_repo(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/contents"
    response = requests.get(url)

    if response.status_code == 200:
        files = response.json()
        python_files = [file_info["name"]
                        for file_info in files if file_info["name"].endswith(".py")]
        json_files = [file_info["name"]
                      for file_info in files if file_info["name"].endswith(".json")]
        return python_files, json_files
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
    parts = REPO_URL.strip("/").split("/")
    owner, repo_name = parts[-2], parts[-1]
    python_files, json_files = list_files_in_repo(owner, repo_name)

    try:
        print(art)
        print("Navi> Welcome to the Chip Market: \nHere you will find community contributed custom scripts...\n\nNavi>Current files in the repository:")
        for file_name in python_files:
            print(f"[PY] {file_name}")
        for file_name in json_files:
            print(f"[JSON] {file_name}")

        download_dir = "/opt/Navi/commands"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        download = input(
            "\nNavi> Enter the filename to download (leave blank to skip): ").strip()
        if download:
            if download in python_files or download in json_files:
                file_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/main/{download}"
                if download.endswith(".json"):
                    download_dir = JSON_DOWNLOAD_DIR
                elif download.endswith(".py"):
                    download_dir = PYTHON_DOWNLOAD_DIR
                else:
                    print(
                        f"Navi> File type not supported for '{download}'. Skipping.")
                    return
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                download_file(file_url, download, download_dir)
                print(
                    f"Navi> '{download}' has been downloaded to {download_dir}.")
            else:
                print(f"Navi> File '{download}' not found in the repository.")
    except Exception as e:
        print(f"Error: {e}")
