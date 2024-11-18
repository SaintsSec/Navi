import requests
import os
import textwrap
import random
import time
import commands
import json
import config
import spacy
import platform

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from mods import mods


class NaviApp:
    art: str = mods.art
    helpAr: str = mods.helpArt
    breakline: str = mods.breakline
    ai_name_rep: str = "Navi> "

    server: str = config.server
    port: int = config.port
    local: str = config.local

    script_dir = os.path.dirname(os.path.abspath(__file__))
    hist_file = os.path.join(script_dir, ".navi_history")

    # NLP setup
    nlp: spacy.language.Language = spacy.load("en_core_web_sm")
    ruler: spacy.pipeline.EntityRuler = nlp.add_pipe("entity_ruler")

    user: str = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NaviApp, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def setup_history(self) -> None:
        self.session = PromptSession(history=FileHistory(self.hist_file))

    def get_user(self) -> str:
        return self.user

    def set_user(self, sys_user: str) -> None:
        self.user = sys_user

    def print_message(self, text: str, include_ai_name: bool = True) -> None:
        to_print = text
        if include_ai_name:
            to_print = self.ai_name_rep + text
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
        lines = to_print.split('\n')

        for line in lines:
            # Wrap each line individually
            wrapped_lines = textwrap.fill(line, width=wrap_width)
            for char in wrapped_lines:
                print(char, end="", flush=True)
                random_num = random.uniform(0, 1)   # nosec
                for range_tuple, sleep_time in sleep_times.items():
                    if range_tuple[0] <= random_num < range_tuple[1]:
                        time.sleep(sleep_time)
                        break
            # Print a newline character after each wrapped line
            print()

    def clear_terminal(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.art)

    def llm_chat(self, user_message: str, called_from_app: bool = False) -> tuple[str, int]:
        # Define the API endpoint and payload
        message_amendment = user_message
        if not called_from_app:
            message_amendment = (
                        ("If the user message has a terminal command request, provide the following 'TERMINAL OUTPUT {"
                         "terminal code to execute request (no not encapsulate command in quotes)}' and NOTHING "
                         "ELSE. Otherwise continue to communicate"
                         "normally.") +
                        f"The user's OS is {platform.system()}" + ". User message:")
        message_amendment += user_message
        url = f"http://{self.server}:{self.port}/api/chat"
        payload = {
            "model": "navi-cli",
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
                    self.print_message(f"Keyboard interrupt registered, talk soon {self.user}!")

            # Concatenate the extracted messages
            full_response = "".join(extracted_responses)
            return full_response, 200
        else:
            return f"{response.url},{response.json()}", 400

    def process_message(self, user_message: str) -> None:
        processed_message = self.nlp(user_message.strip())
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
            response_message, http_status = self.llm_chat(user_message)
            if response_message.startswith("TERMINAL OUTPUT"):
                commands.modules["navi_sys"].run(response_message)
            else:
                self.print_message(f"{response_message if http_status == 200 else 'Issue with server'}")

    def chat_with_navi(self) -> None:
        while True:
            # Get user input
            try:
                user_message = self.session.prompt(f"\n{self.user}> ")
            except EOFError:
                self.print_message("Encountered an unexpected end of input.")
                break
            self.process_message(user_message)

    def setup_navi_vocab(self) -> None:
        # Register commands and aliases with the entity ruler
        for command, module in commands.modules.items():
            patterns = [{"label": "NAVI_COMMAND", "pattern": command}]
            aliases = getattr(module, 'aliases', [])  # Safely get the aliases attribute, default to an empty list
            for alias in aliases:
                patterns.append({"label": "NAVI_COMMAND", "pattern": alias})
            self.ruler.add_patterns(patterns)


navi_instance = NaviApp()
