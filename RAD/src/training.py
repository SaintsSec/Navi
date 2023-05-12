# Imports.
import os
import random
import json
import pickle
import numpy as np
import nltk
from keras.models import Sequential
from nltk.stem import WordNetLemmatizer
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

# Compile and clean the training data.
os.system("rm ./training-data.json")
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
model.add(Dense(128, input_shape=(len(train_x[0]), ),
				activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),
				activation='softmax'))

# Compiling the model
sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
			optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y),
				epochs=850, batch_size=5, verbose=1)

# Saving the model
model.save("echo.h5", hist)

# Print statement to show the
# Successful training of the Chatbot model
print("\nTraining session complete.")