import requests
import os
import getpass
import random
import time
import commands
import argparse
import importlib.util
import json
import config
import re
import spacy

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
    for char in text:
        print(char, end="", flush=True)
        random_num = random.uniform(0, 1)
        for range_tuple, sleep_time in sleep_times.items():
            if range_tuple[0] <= random_num < range_tuple[1]:
                time.sleep(sleep_time)
                break


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
        return f"{ai_name_rep} - [!!] You are running the latest version"


def check_version():
    current_version = "0.1.5"  # Replace with your actual current version
    repo_owner = "SaintsSec"  # Replace with the actual owner name
    repo_name = "Navi"  # Replace with the actual repository name

    result = check_for_new_release(current_version, repo_owner, repo_name)
    print(result)


def pre_run():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(art)


def llm_chat(user_message):
    # Define the API endpoint and payload
    url = f"http://{server}:{port}/api/chat"
    payload = {
        "model": "envoy",
        "messages": [{"role": "user", "content": user_message}]
    }
    headers = {'Content-Type': 'application/json'}
    # Send the POST request
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
        return (full_response,200)
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
        if navi_commands:
            commands.modules[navi_commands[0].text].run(processed_message)
        else:
            response_message, http_status = llm_chat(user_message)
            tr(f"{ai_name_rep} {response_message if http_status == 200 else some_other_message}")
            

# Add all known commands as patterns
def setup_navi_vocab():
    for installed_commands in commands.modules.keys():
        patterns = [{"label": "NAVI_COMMAND", "pattern": installed_commands}]
        ruler.add_patterns(patterns)


def main():
    try:
        pre_run()
        check_version()
        tr(f"{ai_name_rep} How can I help you {user}")
        setup_navi_vocab()
        chat_with_navi()
    except KeyboardInterrupt:
        tr(f"\n{ai_name_rep} Keyboard interupt has been registered, talk soon {user}!")
        exit(0)


if __name__ == "__main__":
    main()
