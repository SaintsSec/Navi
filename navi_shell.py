import requests
import os
import sys
import getpass
import textwrap
import random
import time
import commands
import argparse
import importlib.util
import json
import config
import re
import spacy
import platform
import subprocess
import zipfile
import shutil

from mods import mods

art = mods.art
helpArt = mods.helpArt
user = getpass.getuser()
breakline = mods.breakline
ai_name_rep = "Navi> "

server = config.server
port = config.port

# NLP setup
nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler")


def get_ai_name():
    return ai_name_rep


def get_user():
    return user


def tr(text):
    sleep_times = {
        (0, 0.1): 0.0,
        (0.1, 0.2): 0.05,
        (0.2, 1.0): 0.01
    }

    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        # If we cannot get the terminal size, use a default width
        terminal_width = 80
    # Adjust the wrap width based on 60% of the terminal width
    wrap_width = int(terminal_width * 0.6)

    # Split text into lines to preserve line breaks
    lines = text.split('\n')

    for line in lines:
        # Wrap each line individually
        wrapped_lines = textwrap.fill(line, width=wrap_width)
        for char in wrapped_lines:
            print(char, end="", flush=True)
            random_num = random.uniform(0, 1)
            for range_tuple, sleep_time in sleep_times.items():
                if range_tuple[0] <= random_num < range_tuple[1]:
                    time.sleep(sleep_time)
                    break
        # Print a newline character after each wrapped line
        print()


def get_latest_release(repo_owner, repo_name, edge=False):
    if edge:
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    else:
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if edge:
            for release in data:
                if release['prerelease']:
                    return {
                        'tag_name': release.get('tag_name'),
                        'release_name': release.get('name'),
                        'html_url': release.get('zipball_url')
                    }
        else:
            return {
                'tag_name': data.get('tag_name'),
                'release_name': data.get('name'),
                'html_url': data.get('zipball_url')
            }
    return None


def is_new_release(current_version, latest_version):
    return current_version < latest_version


def check_for_new_release(current_version, repo_owner, repo_name, edge=False):
    latest_release = get_latest_release(repo_owner, repo_name, edge)

    if latest_release and is_new_release(current_version, latest_release['tag_name']):
        return f"New release available!!\n{latest_release['release_name']} ({latest_release['tag_name']})\nURL: {latest_release['html_url']}\n", latest_release['html_url']
    else:
        return "You are running the latest version", None

def update_script(download_url):
    print("Updating the script...")
    try:
        # Download the latest version
        response = requests.get(download_url)
        zip_path = "latest_version.zip"

        with open(zip_path, 'wb') as file:
            file.write(response.content)

        # Unzip the downloaded file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("latest_version")

        # Find the path of the current script
        current_script_path = os.path.abspath(sys.argv[0])
        print(f"Current script path: {current_script_path}")

        # Copy all files from the extracted archive to the current directory
        extracted_dir = os.path.join("latest_version", os.listdir("latest_version")[0])
        for item in os.listdir(extracted_dir):
            s = os.path.join(extracted_dir, item)
            d = os.path.join(os.getcwd(), item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        # Clean up
        shutil.rmtree("latest_version")
        os.remove(zip_path)

        print("Update successful. Restarting the script...")

        # Restart the script with a flag to skip the update check
        os.execv(sys.executable, [sys.executable] + sys.argv + ["--skip-update"])

    except Exception as e:
        print(f"Update failed: {e}")



def check_version(edge=False):
    current_version = "0.1.5" # Note: This isn't a great way to check for updates
    repo_owner = "SaintsSec"
    repo_name = "Navi"

    result, download_url = check_for_new_release(current_version, repo_owner, repo_name, edge)
    print(result)

    return download_url


def pre_run():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(art)


def llm_chat(user_message):
    # Define the API endpoint and payload
    message_amendment = (("If the user message has a terminal command request, provide the following 'TERMINAL OUTPUT {"
                          "terminal code to execute request (no not encapsulate command in quotes)}' and NOTHING "
                          "ELSE. Otherwise continue to communicate"
                          "normally.") +
                         f"The user's OS is {platform.system()}" + ". User message:")
    message_amendment += user_message
    url = f"http://{server}:{port}/api/chat"
    payload = {
        "model": "envoy",
        "messages": [{"role": "user", "content": message_amendment}]
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, json=payload)

    # Check if the response is valid
    if response.status_code == 200:
        response_text = response.text

        # Split the response into lines and parse each line as JSON
        messages = [line for line in response_text.split('\n') if line]
        extracted_responses = []

        for msg in messages:
            try:
                json_msg = json.loads(msg)
                if json_msg.get('message', {}).get('role') == 'assistant':
                    extracted_responses.append(json_msg['message']['content'])
            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)
            except KeyboardInterrupt:
                tr(f"{ai_name_rep} Keyboard interupt registered, talk soon {user}!")

        # Concatenate the extracted messages
        full_response = "".join(extracted_responses)
        return (full_response, 200)
    else:
        return (f"{response.url},{response.json()}", 400)


def chat_with_navi():
    while True:
        # Get user input
        try:
            user_message = input(f"\n{user}> ")
        except EOFError:
            tr("Navi> Encountered an unexpected end of input.")
            break
        processed_message = nlp(user_message.strip())
        navi_commands = [ent for ent in processed_message.ents if ent.label_ == "NAVI_COMMAND"]
        # Check if the message is a question
        question_keywords = {"is", "does", "do", "what", "when", "where", "who", "why", "what", "how"}
        is_question = any(token.text.lower() in question_keywords for token in processed_message if token.i == 0)

        if navi_commands and not is_question:
            command = navi_commands[0].text
            main_command = commands.alias_to_command.get(command)
            if main_command:
                commands.modules[main_command].run(processed_message)
        else:
            response_message, http_status = llm_chat(user_message)

            if response_message.startswith("TERMINAL OUTPUT"):
                commands.modules["navi_sys"].run(response_message)
            else:
                tr(f"{ai_name_rep} {response_message if http_status == 200 else 'Issue with server'}")


# Add all known commands as patterns
def setup_navi_vocab():
    # Register commands and aliases with the entity ruler
    for command, module in commands.modules.items():
        patterns = [{"label": "NAVI_COMMAND", "pattern": command}]
        aliases = getattr(module, 'aliases', [])  # Safely get the aliases attribute, default to an empty list
        for alias in aliases:
            patterns.append({"label": "NAVI_COMMAND", "pattern": alias})
        ruler.add_patterns(patterns)


def main():
    parser = argparse.ArgumentParser(description='Check for new releases and handle updates.')
    parser.add_argument('--edge', action='store_true', help='Check for the edge version')
    parser.add_argument('--noupdate', action='store_true', help='Do not check for updates')
    parser.add_argument('--update', action='store_true', help='Update the script to the latest version if available')
    parser.add_argument('--skip-update', action='store_true', help='Skip the update check (used internally to prevent update loop)')

    args = parser.parse_args()
    if not args.noupdate and not args.skip_update:
        download_url = check_version(args.edge)
        if download_url:
            update_script(download_url)
    try:
        pre_run()
        tr(f"{ai_name_rep} How can I help you {user}")
        setup_navi_vocab()
        chat_with_navi()
    except KeyboardInterrupt:
        tr(f"\n{ai_name_rep} Keyboard interrupt has been registered, talk soon {user}!")
        exit(0)


if __name__ == "__main__":
    main()
