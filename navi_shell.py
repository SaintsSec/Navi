import os
import sys
import getpass
import argparse
import navi_internal
from navi_updater import check_version, update_script

user = getpass.getuser()


def restart_navi():
    os.execv(sys.executable, [sys.executable] + sys.argv + ["--skip-update"])

def check_version(edge=False):
    current_version = "0.5.2"  # Note: This isn't a great way to check for updates
    repo_owner = "SaintsSec"
    repo_name = "Navi"

    result, download_url = check_for_new_release(current_version, repo_owner, repo_name, edge)
    print(result)

    return download_url


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(art)


def llm_chat(user_message, called_from_app=False):
    # Define the API endpoint and payload
    message_amendment = user_message
    if not called_from_app:
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
                print_message(f"Keyboard interupt registered, talk soon {user}!")

        # Concatenate the extracted messages
        full_response = "".join(extracted_responses)
        return full_response, 200
    else:
        return f"{response.url},{response.json()}", 400


def chat_with_navi():
    while True:
        # Get user input
        try:
            user_message = input(f"\n{user}> ")
        except EOFError:
            print_message("Encountered an unexpected end of input.")
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
                print_message(f"{response_message if http_status == 200 else 'Issue with server'}")


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
    navi_instance = navi_internal.navi_instance
    parser = argparse.ArgumentParser(description='Check for new releases and handle updates.')
    parser.add_argument('--edge', action='store_true', help='Check for the edge version')
    parser.add_argument('--noupdate', action='store_true', help='Do not check for updates')
    parser.add_argument('--update', action='store_true', help='Update the script to the latest version if available')
    parser.add_argument('--skip-update', action='store_true',
                        help='Skip the update check (used internally to prevent update loop)')
    parser.add_argument('--install', action='store_true', help='installs Navi based on the current downloaded version.')

    args = parser.parse_args()
    if not args.noupdate and not args.skip_update:
        download_url = check_version(args.edge)
        if download_url:
            update_script(download_url)
    if args.install:
        os.system('cd ./install && ./install.sh')
    try:
        navi_instance.setup_navi_vocab()
        navi_instance.set_user(user)
        navi_instance.clear_terminal()
        navi_instance.chat_with_navi()
        navi_instance.print_message(f"How can I help you {user}")
    except KeyboardInterrupt:
        navi_instance.print_message(f"\nKeyboard interrupt has been registered, talk soon {user}!")
        exit(0)


if __name__ == "__main__":
    main()
