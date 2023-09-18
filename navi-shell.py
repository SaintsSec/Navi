import requests
import subprocess
import os
import getpass
import commands
import argparse
import importlib.util
from mods import mods


art = mods.art
helpArt = mods.helpArt
user = getpass.getuser()
breakline = mods.breakline

ai_name_rep = "Navi> "


def parse_arguments():
    """Parse command-line arguments and return the parsed args object."""

    # Custom formatter that retains any whitespace in the description or epilog.
    parser = argparse.ArgumentParser(
        description="Navi shell arguments.", formatter_class=argparse.RawTextHelpFormatter)

    # Help and usage strings
    q_help = (
        "Quickly query the AI and print the response.\n"
        "Use: navi -q \"Hello there\""
    )

    nh_help = (
        "List currently installed Navi custom scripts.\n"
        "Use: navi -nh"
    )

    r_help = (
        "Run a Navi custom script.\n"
        "Use: navi -r /<command>"
    )

    parser.add_argument('-q', type=str, help=q_help)
    parser.add_argument('-nh', action='store_true', help=nh_help)
    parser.add_argument('-r', type=str, help=r_help)

    # Add other arguments as necessary
    return parser.parse_args()


def handle_arguments(args):
    """Handle the actions based on the provided arguments."""
    if args.q:
        query_rasa_and_print(args.q)
        return True  # Indicate that we've handled an argument and may not need to proceed to the main chat

    if args.r:
        # Handle the -r argument logic here
        if args.r in commands.modules.keys():
            print(
                f"{mods.breakline}\n{ai_name_rep} [\u2713] - Running command: '{args.r}'\n{mods.breakline}")
            commands.modules[args.r].run()
        return True

    if args.nh:
        directory_path = '/opt/Navi/commands'

        # Filter for Python files and exclude __init__.py
        files = [f for f in os.listdir(directory_path) if f.endswith(
            '.py') and f != '__init__.py']

        commands_and_uses = []

        for file in files:
            command = file.replace('.py', '')

            # Load the module
            spec = importlib.util.spec_from_file_location(
                command, os.path.join(directory_path, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Grab the 'use' variable from the module
            # Default to 'Description not found' if 'use' is not in the script
            use_desc = getattr(module, 'use', 'Description not found')
            commands_and_uses.append((command, use_desc))

        # For alignment purposes
        max_command_length = max([len(cmd) for cmd, _ in commands_and_uses])
        max_use_length = max([len(use) for _, use in commands_and_uses])

        print("\nCurrently installed Navi custom scripts:\n")
        print(f"{'Command':<{max_command_length}} \t Description")
        print('-' * max_command_length + '\t' + '-' *
              max_use_length)  # Drawing separators

        for command, use_desc in commands_and_uses:
            print(f"{command:<{max_command_length}} \t {use_desc}")

        print("\nuse navi -r /<command> to run a script")
        return True

    return False  # Indicate that no specific argument actions were handled


def is_rasa_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        pass
    return False


def preRun():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print(art)

# Navi Script Engine


def chip_engine_help():
    print(f"""{helpArt}
Navi is a simple to use customizable interface for CLI
AI models. Built with cybersecurity professionals in mind. 

[!!] - All commands are preceeded by a '/'
Here is a list of current useable commands 

from the main interface typing 'ohce config' will allow you to
configure the AI to your liking.

Command:              Use:
""")
    for _, module in commands.modules.items():
        print(module.command.ljust(21), module.use)
    print(breakline)


def chip_engine():
    chip_engine_help()
    message = input(f"{ai_name_rep} What do you want to run:  ")
    if message[0] == "/":
        if message in commands.modules.keys():
            print(
                f"{mods.breakline}\n{ai_name_rep} [\u2713] - Running command: '{message}'\n{mods.breakline}")
            commands.modules[message].run()
        if message == "":
            print(
                f"{ai_name_rep} [!!] - I did not catch that. Please try again.")


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
        return f"{ai_name_rep} - [!!] New release available!!\n{latest_release['release_name']} ({latest_release['tag_name']})\nURL: {latest_release['html_url']}\n"
    else:
        return f"{ai_name_rep} - [!!] You are running the latest version!\n"


def checkVersion():
    current_version = "0.1.2"  # Replace with your actual current version
    repo_owner = "SSGOrg"  # Replace with the actual owner name
    repo_name = "Navi"  # Replace with the actual repository name

    result = check_for_new_release(current_version, repo_owner, repo_name)
    print(result)


def query_rasa_and_print(query):
    url = "http://localhost:5005/webhooks/rest/webhook"
    data = {"sender": "user", "message": query}
    response = requests.post(url, json=data)

    response_data = response.json()
    if isinstance(response_data, list) and response_data and 'text' in response_data[0]:
        message_text = response_data[0]['text']
        formatted_response = f"{ai_name_rep} {message_text}"
        print(formatted_response)
    else:
        print(f"{ai_name_rep} I'm sorry, I couldn't understand that.")


def chat_with_rasa(initial_query=None):
    url = "http://localhost:5005/webhooks/rest/webhook"

    if initial_query:
        query_rasa_and_print(initial_query)
        return

    while True:
        # Get user input
        try:
            user_message = input(f"{user}> ")
        except EOFError:
            print("Encountered an unexpected end of input.")
            break

        # Exit loop if the user types 'exit' or 'quit'
        if user_message.lower() in ['/stop', 'quit']:
            print(f"{ai_name_rep} Goodbye!")
            break
        if user_message.lower() in ['/clear', 'cls']:
            preRun()
            print(f"{ai_name_rep} How can I help you {user}")
            continue
        if user_message.lower() in ['run', 'chips', 'execute']:
            chip_engine()

        # Send user message to Rasa
        data = {"sender": "user", "message": user_message}
        response = requests.post(url, json=data)

        # Parse the JSON response
        response_data = response.json()

        # Check if response_data is a list, it's not empty, and the first item has the 'text' key
        if isinstance(response_data, list) and response_data and 'text' in response_data[0]:
            # Extract the 'text' from the 'messages' list
            message_text = response_data[0]['text']

            # Format and print Rasa's response
            formatted_response = f"{ai_name_rep} {message_text}"
            print(formatted_response)
        else:
            print(f"{ai_name_rep} I'm sorry, I couldn't understand that.")


def main():
    args = parse_arguments()
    if handle_arguments(args):
        return

    preRun()
    checkVersion()
    print(f"{ai_name_rep} How can I help you {user}")
    chat_with_rasa()


if __name__ == "__main__":
    main()
