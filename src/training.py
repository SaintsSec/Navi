# Imports.
import json
import nltk
import numpy as np
import os
import pickle
import random
import sys
import time
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.layers import Activation, Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam, SGD
from nltk.stem import WordNetLemmatizer

breakline = "+===================================================+"
art = """
  ______           _       _                _____           _       __ 
 /_  __/________ _(_)___  (_)___  ____ _   / ___/__________(_)___  / /_
  / / / ___/ __ `/ / __ \/ / __ \/ __ `/   \__ \/ ___/ ___/ / __ \/ __/
 / / / /  / /_/ / / / / / / / / / /_/ /   ___/ / /__/ /  / / /_/ / /_  
/_/ /_/   \__,_/_/_/ /_/_/_/ /_/\__, /   /____/\___/_/  /_/ .___/\__/  
                               /____/                    /_/           
"""

# Pre-run.
os.system("clear")
user = os.getlogin()
print(art)
# Hide tracebacks - change to 1 for dev mode.
sys.tracebacklimit = 0
def type_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)  # Adjust the sleep duration as desired
    print()

try:
	# Asks training variables.
	naviText = "Navi> In order to get the most out of me, you need to train me. How many cycles or epochs do you want?"
	type_text(naviText)
	epv = int(input("Number of Epochs: "))
	naviText = "\nNavi> I come with two training models each serving its own purpose SGD and Adam... Pick one."
	type_text(naviText)
	tmv = input("SGD or Adam: ").lower()
	naviText = "Navi> Lets plug this brain in and boot it up! Beginning training sequence now!"
	type_text(naviText)
	print(breakline)

	# Compile and clean the training data.
	directory = "intenses_db/"
	data = []
	for filename in os.listdir(directory):
		if filename.endswith(".json"):
			# Open the file and load the JSON data
			with open(directory + filename, "r") as f:
				file_data = json.load(f)
			# Append the data to the list
			data.append(file_data)
	with open(directory + "training-data.json", "w") as f:
		json.dump(data, f, indent=4)
	os.system("rm ./training-data.json")
	os.system("mv ./intenses_db/training-data.json training-data.txt")
	
	with open('training-data.txt', 'r') as f:
		file_contents = f.close()
	
	# Modify the file.
	with open('training-data.txt', 'r') as file:
		data = file.read()
	
	# Replace the target.
	data = data.replace('        ]\n    },\n    {\n        "intents": [', '            ,')
	
	with open('training-data.txt', 'w') as file:
		file.write(data)
	
	# Trims excess.
	with open("training-data.txt", "r") as f:
		lines = f.readlines()
	
	# Remove last line.
	lines = lines[1:-1]
	
	with open("training-data.txt", "w") as f:
		f.writelines(lines)
	
	# Convert to json.
	os.system("mv ./training-data.txt ./training-data.json")
	
	# Reading the training-data.json file
	lemmatizer = WordNetLemmatizer()
	# Reading the json.intense file
	intents = json.loads(open("training-data.json").read())
	
	# Creating empty lists to store data
	words = []
	classes = []
	documents = []
	ignore_letters = ["?", "!", ".", ","]
	for intent in intents['intents']:
		for pattern in intent['patterns']:
			# Separating words from patterns
			word_list = nltk.word_tokenize(pattern)
			words.extend(word_list) # and adding them to words list
			
			# Associating patterns with respective tags
			documents.append((word_list, intent['tag']))
	
			# Appending the tags to the class list
			if intent['tag'] not in classes:
				classes.append(intent['tag'])
	
	# Storing the root words or lemma
	words = [lemmatizer.lemmatize(word)
			for word in words if word not in ignore_letters]
	words = sorted(set(words))
	
	# Saving the words and classes list to binary files
	pickle.dump(words, open('words.pkl', 'wb'))
	pickle.dump(classes, open('classes.pkl', 'wb'))
	
	training = []
	output_empty = [0]*len(classes)
	for document in documents:
		bag = []
		word_patterns = document[0]
		word_patterns = [lemmatizer.lemmatize(
			word.lower()) for word in word_patterns]
		for word in words:
			bag.append(1) if word in word_patterns else bag.append(0)
	
		# Making a copy of the output_empty
		output_row = list(output_empty)
		output_row[classes.index(document[1])] = 1
		training.append([bag, output_row])
	random.shuffle(training)
	training = np.array(training, dtype=object)
	
	# Splitting the data
	train_x = list(training[:, 0])
	train_y = list(training[:, 1])

	# Creating a Sequential machine learning model
	model = Sequential()
	model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(128, activation='relu'))
	model.add(Dropout(0.2))
	model.add(Dense(len(train_y[0]), activation='softmax'))

	# Create a TensorBoard callback!
	tensorboard_callback = TensorBoard(log_dir='./tlogs', histogram_freq=1, write_graph=True, write_images=True)

	# Compiling the model.
	if tmv == "sgd":
		optimizer = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
	if tmv == "adam":
		optimizer = Adam(lr=0.001, decay=1e-6)

	model.compile(loss='categorical_crossentropy', optimizer=tmv, metrics=['accuracy'])

	# Fit the model with TensorBoard callback
	hist = model.fit(np.array(train_x), np.array(train_y), epochs=epv, batch_size=5, verbose=1, callbacks=[tensorboard_callback])

	# Saves the model.
	model.save("echo.h5", hist)

	# Prints training complete and opens web panel.
	print(breakline)
	naviChoice = f"Navi> Oh wow {user}! I feel smarter... Do you wish to see the output of the training I just did?"
	type_text(naviChoice)
	tensorChoice = input("Yes or No? ").lower()
	if tensorChoice == "yes":
		naviText = "Navi> Understood, I will get that booted up for you now!"
		type_text(naviText)
		os.system("tensorboard --logdir=./tlogs --port=6006")
	if tensorChoice == "no":
		naviText = "Navi> Shame! But I guess you are in a rush, I cant blame you. Next time you run the training script check it out!"
		type_text(naviText)
	else:
		naviText = "Navi> That is not an option, try again next time!"
		type_text(naviText)

	naviText = f"\nNavi> Training complete! \nNavi> Now to run me... restart the terminal and type navi into the command prompt. \n\nNavi> I look forward to working with you {user}!"
	type_text(naviText)
except json.decoder.JSONDecodeError as e:
	print("\n[!] Error decoding JSON or training data:", e)
