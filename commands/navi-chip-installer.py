import requests
from navi import get_parameters
from navi_shell import print_message

command = "chips"
use = "Manage Navi chips"


def get_latest_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    response = requests.get(url)

    if response.status_code == 200:
        release = response.json()
        return release.get('tag_name', 'No release found')
    else:
        return 'No release found'


def truncate_string(input_string, max_length=10):
    if len(input_string) > max_length:
        return input_string[:max_length] + "..."
    return input_string


def search_repos_by_topic_and_name(topic, name=None, per_page=10, page=1):
    base_url = "https://api.github.com/search/repositories"
    query = f"topic:{topic}"

    if name:
        query += f"+{name} in:name"

    url = f"{base_url}?q={query}&per_page={per_page}&page={page}"

    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json().get('items', [])
        if not repos:
            print("No Navi Chips found.")
            return
        available_repos = 0
        for repo in repos:
            owner = repo['owner']['login']
            repo_name = repo['name']
            repo_description = truncate_string(repo['description'])
            latest_release = get_latest_release(owner, repo_name)
            if latest_release != "No release found":
                available_repos += 1
                print(f"Name: {repo_name}, Description: {repo_description}, Latest Release: {latest_release}")
        if available_repos == 0:
            print("No Navi Chips found with releases.")
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")
        print(response.json())


def help_text():
    print_message("Chip Manager\n"
                  "chips [install | uninstall | search]\n\n"
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
        print("Listing installed apps")
        return
    if len(argv) == 1:
        print("ABOUT THE CHIP")
        return

    if command == "install" and len(argv) > 1:
        print(f"Install app {argv[1]}")
        return

    if command == "uninstall" and len(argv) > 1:
        print(f"Uninstall app {argv[1]}")
        return

    if command == "search" and len(argv) > 1:
        search_repos_by_topic_and_name("navi-chips", argv[1])
        return

    help_text()

    # help list -> List out installed apps
    # manage -> chips {app name} {OPTIONAL: install || uninstall}
    # chips {app name} -> Installed version | Latest version | Author | Description | Repo URL | To
    # install, type "chips {app} install
