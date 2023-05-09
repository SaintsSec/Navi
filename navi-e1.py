import speech_recognition as sr # Recognizing speech from audio input.
import pyttsx3 # Text-to-speech conversion.
import random # Replacing with URandom, to generate random responses from the list of possible responses.
import json # Used for handling JSON data.
import pickle # Used in serializing and deserializing Python objects.
import numpy as np # Used for working with arrays and mathematical operations.
import nltk # Used for natural/neural language processing tasks like tokenization, stemming, lemmatization, and POS tagging.
import psutil #  used for getting system information like CPU utilization, memory usage, and disk usage. This is how the AI finds its 'wellness_value'.
from keras.models import load_model # Used to load a trained model from the training program.
from nltk.stem import WordNetLemmatizer # Used in lemmatization.
import threading
from mods import mods
import commands

# Instantiate WordNetLemmatizer for lemmatization.
lemmatizer = WordNetLemmatizer()
# Load intents from the training data file.
intents = json.loads(open("src/training-data.json").read())
# Load preprocessed words and classes from pickle files.
words = pickle.load(open('src/words.pkl', 'rb'))
classes = pickle.load(open('src/classes.pkl', 'rb'))
# Load the trained model from disk.
model = load_model('src/echo.h5')

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

# Function to play audible output using pyttsx3 library.
def speak(audio):
    # Initializes the pyttsx3 engine.
    engine = pyttsx3.init()
    # Gets properties of the engine.
    volume = engine.getProperty('volume')
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    # Sets properties of the engine.
    engine.setProperty('voice', voices[1].id) # Set the voice to the second voice (in the list of voices).
    engine.setProperty('volume', 10) # Set the volume to 10.
    engine.setProperty('rate', 165) # Set the speaking rate to 165.
    # Uses the engine to speak the input audio.
    engine.say(audio)
    engine.runAndWait()

# Wellness module.
def get_wellness():
    # Get CPU usage percentage.
    cpu = psutil.cpu_percent()
    # Get virtual memory usage percentage.
    memory = psutil.virtual_memory()[2]
    # Get disk usage percentage.
    disk = psutil.disk_usage('/').percent
    # Calculate average usage percentage.
    avg = (cpu + memory + disk) / 3
    # AI wellness value.
    wellness_value = avg
    # AI is well.
    if wellness_value < 30:
        responses = ["I'm feeling great today!", "Couldn't be better!", "I'm doing well, thank you."]
    # AI is neutral.
    elif wellness_value >= 30 and wellness_value < 70:
        responses = ["I'm doing okay, thank you.", "I'm hanging in there.", "I'm feeling so-so today."]
    # AI is unwell.
    else:
        responses = ["I'm not feeling so great today.", "I could be better.", "I'm struggling a bit today."]
    # Choose a response at random from the possible responses.
    response = random.choice(responses)
    print(response)
    print("\nWellness value:",int(wellness_value))
    speak(response)

# Kills on kill request.
def killswitch():
    speak("Please hold, I'm shutting down.")
    exit()

# Tidy up.
ai_name = "Navi-E1"
ai_name_rep = "Navi-E1>"

# Taking a vocal command.
def takeCommand():
    # Initializes a recognizer instance
    r = sr.Recognizer()
    # Configures the microphone as the source of audio input.
    with sr.Microphone() as source:
        # Adjusts the recognizer to the ambient noise level.
        r.adjust_for_ambient_noise(source)
        # Sets the pause threshold to 0.5 seconds of non-speaking audio before a phrase is considered complete.
        r.pause_threshold = 0.5
        # Captures the audio input from the microphone.
        audio = r.listen(source)
        try:
            # Attempts to recognize the speech in the captured audio using Google Speech Recognition API.
            message = r.recognize_google(audio, language='en-in')
            # Prints the recognized speech message.
            print(f"{ai_name} heard:", message)
        except Exception as e:
            # Prints the error message if there's any problem in recognizing speech.
            print(e)
            return "None"
    # Returns the recognized speech message.
    return message

def AI():
    # Run forever, until cancelled.
    mods.clearScreen()
    print(mods.art)
    print("Ready to assist.")
    speak("Ready to assist.")
    while True:
        try:
            message = ""# If uncommented, it'll always respond without a wake word!
            #message = takeCommand() # Uncomment if you wish to speak to wake it.

            # Check if wake words have been spoken.
            if "" in message or "Hey Navi" in message: # Wake words.

                # Message to the 'AI'.
                print("\nNavi> I am listening!")

                message = input("=> ").lstrip() # If uncommented, it'll take an input sentence instead of voice!
                # message = takeCommand() # Uncomment if you wish to speak to wake it.

                # Precoded commands.
                if message[0] == '/':
                    print(mods.breakline)
                    if message == "/stop":
                        print("Navi> [!!] - I look forward to seeing you again!")
                        print(mods.breakline)
                        exit(0)
                    if message == "/clear":
                        mods.clearScreen()
                        print(mods.art)
                    elif message in commands.modules.keys():
                        print("Navi> [!!] - Runing command:", message)
                        print(mods.breakline)
                        commands.modules[message].run()
                        print(mods.breakline)
                    else:
                        print(f"Navi> [!!] - Unknown command: '{message}'")
                        print(mods.breakline)
                else:
                # AI segment.
                    if "you feeling" in message or "how do you feel" in message or "how are you feeling" in message:
                        get_wellness()
                    else:
                        # Checks intents / responses.
                        ints = predict_class(message)
                        res = get_response(ints, intents)
                        print(f"{ai_name_rep} ", res)
                        speak(res)
        except KeyboardInterrupt:
            # If the user interrupts the program.
            print(f"Navi> [!!] - I look forward to seeing you again!\n{mods.breakline}")
            exit()

if __name__ == '__main__':
    AI()

# Create a thread for handling the AI.
cleanup_thread = threading.Thread(target=clean_up_sentences)
bag_thread = threading.Thread(target=bagw)
prediction_thread = threading.Thread(target=predict_class)
speak_thread = threading.Thread(target=speak)
command_thread = threading.Thread(target=takeCommand)
wellness_thread = threading.Thread(target=get_wellness)
AI_thread = threading.Thread(target=AI)

# Start both threads.
cleanup_thread.start()
bag_thread.start()
prediction_thread.start()
speak_thread.start()
command_thread.start()
wellness_thread.start()
AI_thread.start()

# Wait for threads to finish before exiting the program.
cleanup_thread.join()
bag_thread.join()
prediction_thread.join()
speak_thread.join()
command_thread.join()
wellness_thread.join()
AI_thread.join()
