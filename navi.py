# Imports.
import datetime
import json
import nltk
import numpy as np
import os
import pickle
import psutil
import pyttsx3
import random
import speech_recognition as sr
import sys
import threading
import subprocess
import requests
from datetime import date
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

import commands
from mods import mods
from mods import typewriter

# Pre-run.
subprocess.run("clear")
sys.tracebacklimit = 0

# Navi Global Vars
breakline = mods.breakline
art = mods.art
helpArt = mods.helpArt
typewriter = typewriter.typewriter

# Loading the configuration json.
with open('./var/pipes/config.json') as config_file:
    config = json.load(config_file)

# Access the variables from the loaded configuration.
ai_name = config['ai']['name']
ai_name_rep = (f"{ai_name}>")
ai_gender = config['gender'][config['ai']['gender']]
ai_volume = config['ai']['volume']
ai_speed = config['ai']['speed']
ai_voice = config['ai']['voice']
operator_name = config['operator']['name']
operator_nicks_list = config['operator']['nicks']
operator_nicks = random.choice(operator_nicks_list)


def ai_config():
    os.system("python3 ./src/modules/config.py")
    exit()


# Logging -- You can ignore this, it's for making 'memories'.
# Sets time and date.
current_time = datetime.datetime.now().strftime("%H:%M:%S")
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
mem_gen = current_date + ".mem"
mem_path = os.path.join("./var/log/memories/", mem_gen)
# Generates 'memories' directory, then creates the dir and file before confirming.
os.makedirs("./var/log/memories/", exist_ok=True)
with open(mem_path, 'w') as file:
    file.write(">> START OF MEMORY <<\n")
if os.path.isfile(mem_path):
    print(f"File '{mem_path}' created successfully.")
else:
    print(f"Failed to create the file '{mem_path}', one might already exist.")
# Allows the reading and writing for 'memories'.
log_file = open(f"./var/log/memories/{date.today()}.mem", "a")
log_file.write(f"SESSION | {date.today()}-{current_time}\n")

# Neural segment -- This is where the AI magic happens.
# Downloads any updates.
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
intents = json.loads(open("src/neural_data/training-data.json").read())
words = pickle.load(open('src/neural_data/words.pkl', 'rb'))
classes = pickle.load(open('src/neural_data/classes.pkl', 'rb'))
model = load_model('src/neural_data/echo.h5')

# Tokenize the words in the sentence and lemmatize them.


def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Convert the sentence to a bag of words representation.


def bagw(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Use the trained model to predict the class of the input sentence.


def predict_class(sentence):
    bow = bagw(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Get a random response from the list of responses associated with the predicted class.


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Functions segment -- This is where the main functions are.


def speak(audio):
    if ai_voice == 'enabled':
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[ai_gender].id)
        engine.setProperty('volume', ai_volume)
        engine.setProperty('rate', ai_speed)
        engine.say(audio)
        engine.runAndWait()
    if ai_voice == 'disabled':
        pass

# Modules segment -- This is where any modules you want to build should be.

# Navi Chip Engine Help


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

# Navi Chip Engine


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
                "Navi> [!!] - I did not catch that. Please try again.")


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
        return f"{ai_name_rep} - [!!] New release available!!\n{latest_release['release_name']} ({latest_release['tag_name']})\nURL: {latest_release['html_url']}"
    else:
        return f"{ai_name_rep} - [!!] You are running the latest version!"


def checkVersion():
    current_version = "0.1.1"  # Replace with your actual current version
    repo_owner = "SSGOrg"  # Replace with the actual owner name
    repo_name = "Navi"  # Replace with the actual repository name

    result = check_for_new_release(current_version, repo_owner, repo_name)
    print(result)

# Wellness.


def get_wellness():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()[2]
    disk = psutil.disk_usage('/').percent
    avg = (cpu + memory + disk) / 3
    wellness_value = avg

    # AI is well.
    if wellness_value < 30:
        responses = [
            "I'm feeling great today!",
            "Couldn't be better!",
            "I'm doing well, thank you.",
            "I feel like a million bucks today!",
            "Life is good today!",
            "I'm on top of the world!",
            "I'm feeling fantastic today!",
            "I'm in a really good mood today.",
            "Today is going to be a great day!",
            "I'm feeling energized today!",
            "I'm feeling awesome and unstoppable!",
            "I'm positively radiant today.",
            "I'm brimming with happiness and positivity!",
            "I'm genuinely excited about today.",
            "I'm enjoying every moment to the fullest!"]
    # AI is neutral.
    elif wellness_value >= 30 and wellness_value < 70:
        responses = [
            "I'm doing okay, thank you.",
            "I'm hanging in there.",
            "I'm feeling so-so today.",
            "I'm just taking it one day at a time.",
            "I'm managing, thank you for asking.",
            "I'm coping.",
            "I'm feeling alright today.",
            "I'm doing my best today.",
            "I'm feeling content today.",
            "I'm feeling balanced today.",
            "I'm maintaining a steady state of mind.",
            "I'm embracing the ebb and flow of the day.",
            "I'm staying composed and focused.",
            "I'm finding a sense of equilibrium.",
            "I'm navigating through with a steady pace."]
    # AI is unwell.
    else:
        responses = [
            "I'm not feeling so great today.",
            "I could be better.",
            "I'm struggling a bit today.",
            "Today is a bit tough for me.",
            "I'm feeling a little down today.",
            "I'm not feeling my best today.",
            "I'm feeling overwhelmed today.",
            "I'm not doing so well today.",
            "I'm feeling stressed today.",
            "I'm feeling anxious today.",
            "I'm facing some challenges at the moment.",
            "I'm going through a bit of a rough patch.",
            "I'm dealing with a mix of emotions today.",
            "I'm finding it hard to lift my spirits.",
            "I'm in need of some self-care and comfort."]

    # Choose a response at random from the possible responses.
    response = random.choice(responses)
    print(f"{ai_name_rep} {response}")
    speak(response)

# Kills on kill request.


def killswitch():
    print(f"{ai_name_rep} Please hold, I'm shutting down.")
    speak("Please hold, I'm shutting down.")
    exit()

# Operational segment -- Responsible for actual operational functionality, such as taking commends, or talking!
# Taking a vocal command.


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            message = r.recognize_google(audio, language='en-in')
            print(f"{ai_name} heard:", message)
        except Exception as e:
            print(e)
            return "None"
    return message


def AI():
    os.system("clear")
    print(f"{art}")
    checkVersion()
    # Run forever, until cancelled.
    while True:
        try:
            # If uncommented, it'll always respond without a wake word!
            message = f"{ai_name}"
            # message = takeCommand(); print(f"\n{ai_name} is listening!") # Uncomment if you wish to speak to wake it.

            # Wake words.
            if f"{ai_name}" in message or f"Hey {ai_name}" in message:
                # If uncommented, it'll take an input sentence instead of voice!
                message = input(f"\n=> ")
                # message = takeCommand() # Uncomment if you wish to speak to wake it.

                # Precoded commands.
                if any(keyword in message for keyword in ["killswitch", "kill switch", "/stop"]):
                    killswitch()
                elif any(keyword in message for keyword in ["how are you", "you feeling", "how do you feel", "how are you feeling"]):
                    get_wellness()
                elif any(keyword in message for keyword in ["ohce config"]):
                    ai_config()
                elif any(keyword in message for keyword in ["nce", "navi chip engine", "chips", "scripts", "execute", "run"]):
                    chip_engine()
                elif any(keyword in message for keyword in ["/clear"]):
                    os.system("clear")
                    print(art)

                # Response segment.
                else:
                    # Checks intents / responses.
                    ints = predict_class(message)
                    res = get_response(ints, intents)
                    # Neural variables -- You can make your own neural variables by adding onto the list, and doing a replace check for a hard-coded variable!
                    if any(neural_variable in res for neural_variable in ["operator_name", "operator_nicks", "ai_name"]):
                        res = res.replace("operator_name", operator_name)
                        res = res.replace("operator_nicks", operator_nicks)
                        res = res.replace("ai_name", ai_name)

                    # Respond appropriately.
                    typewriter(f"{ai_name_rep} {res}")
                    speak(res)

                    # Appends to mems.
                    log_file.write(f"PATTERN  | {operator_name}: {message}\n")
                    log_file.write(f"RESPONSE | {ai_name}: {res}\n")
                    log_file.flush()

        # Error handling.
        except KeyboardInterrupt:
            print("\nInturrupted with keyboard, exiting.")
            exit()
        except FileNotFoundError as e:
            if str(e).endswitch("training-data.json"):
                print("\n[!] The specific file 'training-data.json' is not found.")
            else:
                print("\n[!] File not found.")
        except json.decoder.JSONDecodeError as e:
            print("\n[!] Error decoding JSON or training data:", e)
            sys.exit(1)


if __name__ == '__main__':
    AI()

# Threading segment -- If you make a new def or module, you can thread it.
# Create a thread for handling the AI.
cleanup_thread = threading.Thread(target=clean_up_sentences)
bag_thread = threading.Thread(target=bagw)
prediction_thread = threading.Thread(target=predict_class)
speak_thread = threading.Thread(target=speak)
command_thread = threading.Thread(target=takeCommand)
wellness_thread = threading.Thread(target=get_wellness)
AI_thread = threading.Thread(target=AI)
chip_thread = threading.Thread(target=chip_engine)

# Start both threads.
cleanup_thread.start()
bag_thread.start()
prediction_thread.start()
speak_thread.start()
command_thread.start()
wellness_thread.start()
AI_thread.start()
chip_thread.join()

# Wait for threads to finish before exiting the program.
cleanup_thread.join()
bag_thread.join()
prediction_thread.join()
speak_thread.join()
command_thread.join()
wellness_thread.join()
AI_thread.join()
chip_thread.join()
