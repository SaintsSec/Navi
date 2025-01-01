import json
import os
import platform
import random
import textwrap
import time

import requests
import spacy
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

import chips
import config
import navi_banner


class NaviApp:
    art: str = navi_banner.art
    three_b_art: str = navi_banner.three_b_art
    helpAr: str = navi_banner.helpArt
    breakline: str = navi_banner.breakline
    ai_name_rep: str = "Navi"

    server: str = config.remote
    port: int = config.port
    local: str = config.local

    memory_dir: str = "memories"
    default_session: str = "default.json"
    token_limit: int = 2048
    active_session: str = "DEFAULT_SESSION"

    llm_chat_prompt: str = (
            (
                "YOU ARE A CHATBOT. Communicate like a normal chatbot UNLESS the user has request that explicitly requires the terminal to perform, "
                "in that case,provide the following 'TERMINAL OUTPUT {"
                "terminal code to execute request (no not encapsulate command in quotes)}' and NOTHING "
                "ELSE."
                "normally.") +
            f"The user's OS is {platform.system()}" + ". User message:")

    is_local: bool = True

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

    def set_local(self, local_state) -> None:
        self.is_local = local_state

    def set_navi_name(self, navi_name: str) -> None:
        self.ai_name_rep = navi_name

    def print_message(self, text: str, include_ai_name: bool = True) -> None:
        to_print = text
        if include_ai_name:
            to_print = self.ai_name_rep + "> " + text
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
                random_num = random.uniform(0, 1)  # nosec
                for range_tuple, sleep_time in sleep_times.items():
                    if range_tuple[0] <= random_num < range_tuple[1]:
                        time.sleep(sleep_time)
                        break
            # Print a newline character after each wrapped line
            print()

    def clear_terminal(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        if self.is_local:
            print(self.three_b_art)
        else:
            print(self.art)

    def llm_chat(self, user_message: str, called_from_app: bool = False, call_remote: bool = False) -> tuple[str, int]:
        # Define the API endpoint and payload
        message_amendment = user_message
        if not called_from_app:
            message_amendment = self.llm_chat_prompt
        message_amendment += user_message
        url = f"http://{self.local}:{self.port}/api/chat"
        if call_remote or not self.is_local:
            url = f"http://{self.server}:{self.port}/api/chat"
        chat_history = self.load_session(self.active_session)
        chat_history = self.trim_history_to_token_limit(chat_history, self.token_limit)
        payload = {
            "model": "navi-cli",
            "messages": chat_history + [{"role": "user", "content": message_amendment}]
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
            self.save_chat_to_session(self.active_session, chat_history, {"role": "user", "content": user_message}, {"role": "assistant", "content": full_response}),
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
            main_command = chips.alias_to_command.get(command)
            if main_command:
                chips.modules[main_command].run(processed_message)
        else:
            response_message, http_status = self.llm_chat(user_message)
            if response_message.startswith("TERMINAL OUTPUT"):
                chips.modules["navi_sys"].run(response_message)
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

    def setup_memory(self) -> None:
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
        if not os.path.exists(self.get_session_path("DEFAULT_SESSION")):
            self.create_new_session("DEFAULT_SESSION")

    def get_session_path(self, session_name):
        return os.path.join(self.memory_dir, f"{session_name}.json")

    def trim_history_to_token_limit(self, chat_history, token_limit):
        while chat_history and self.calculate_tokens(chat_history) > token_limit:
            chat_history.pop(0)

        return chat_history

    def load_session(self, session_name):
        path = self.get_session_path(session_name)
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return []

    def save_session(self,session_name, chat_history):
        path = self.get_session_path(session_name)
        with open(path, 'w') as f:
            json.dump(chat_history, f, indent=4)

    def calculate_tokens(self, chat_history):
        return sum(len(entry['content'].split()) for entry in chat_history)

    def create_new_session(self, session_name):
        if not session_name.upper():
            print("Session name cannot be empty.")
            return
        if os.path.exists(self.get_session_path(session_name.upper())):
            print("Session with this name already exists.")
            return
        self.save_session(session_name.upper(), [])

    def set_active_session(self, session_name):
        if not os.path.exists(self.get_session_path(session_name)):
            print(f"Session {session_name} does not exist.")
            return None
        self.active_session = session_name

    def save_chat_to_session(self, session_name, history, chat_user, chat_assistant):
        chat_history = history
        chat_history.append(chat_user)
        chat_history.append(chat_assistant)

        # Handle token overflow
        from navi_shell import get_navi_settings
        if get_navi_settings()["overwrite_session"] and self.calculate_tokens(chat_history) > self.token_limit:
            chat_history.pop(0)

        self.save_session(session_name, chat_history)

    def setup_navi_vocab(self) -> None:
        # Register commands and aliases with the entity ruler
        for command, module in chips.modules.items():
            patterns = [{"label": "NAVI_COMMAND", "pattern": command}]
            aliases = getattr(module, 'aliases', [])  # Safely get the aliases attribute, default to an empty list
            for alias in aliases:
                patterns.append({"label": "NAVI_COMMAND", "pattern": alias})
            self.ruler.add_patterns(patterns)


navi_instance = NaviApp()
