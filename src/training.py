# Imports.
import json
import nltk
import numpy as np
import os
import pickle
import random
import time
import sys
import getpass
from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.layers import Dense, Dropout
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
user = getpass.getuser()
print(art)
# Hide tracebacks - change to 1 for dev mode.
sys.tracebacklimit = 0


def type_text(text):
    for char in text:
        print(char, end="", flush=True,)
        # generate a random number between 0 and 1
        random_num = random.uniform(0, 1)
        # if the random number is less than .1
        if random_num < .1:
            # sleep for 1 second
            time.sleep(.0)
        # else if the rando
        elif random_num < .2:
            # sleep for .5 seconds
            time.sleep(.050)
        # else
        else:
            # sleep for .1 seconds
            time.sleep(.010)


epochExplain = """
Navi> In order to get the most out of me we need to do a little training. This involves Epochs. Epochs are the number of times 
the training cycle will run. The more epochs the more accurate the model will be. Let me explain this a little further: 

In AI training, an epoch refers to a single iteration through the entire dataset during the training process. In other words, 
it is a complete pass of all the training samples in the dataset used to update the model's parameters.

During each epoch, the model is presented with all the training data, and it makes predictions for each sample. 
After the predictions are made, the model's performance is evaluated using a loss function that measures the difference 
between the predicted outputs and the actual targets. The optimizer then adjusts the model's parameters based on the calculated 
gradients, aiming to minimize the loss and improve the model's performance.

Training typically involves running multiple epochs. Each epoch allows the model to learn from the data and refine its 
parameters further, leading to gradual improvement in performance. The number of epochs used in training is a hyperparameter 
that needs to be tuned based on the complexity of the problem, the size of the dataset, and other factors. Too few epochs may 
result in underfitting, while too many epochs may lead to overfitting, where the model memorizes the training data but fails to 
generalize well to new, unseen data.

In summary, an epoch represents one complete iteration through the entire training dataset, allowing the AI model(me) to learn 
from the data and improve its performance with each pass.
"""

trainexplain = """
Navi> I come with two different training algorithms. SGD and Adam. Before we pick one lets talk about them.
SGD (Stochastic Gradient Descent) and Adam (Adaptive Moment Estimation) are both optimization algorithms commonly used in 
training artificial intelligence models, particularly in deep learning.

    SGD (Stochastic Gradient Descent):
        SGD is a simple and widely used optimization algorithm.
        It updates model parameters by taking the average gradient of the loss function for each individual data point 
        (hence, "stochastic"). The learning rate is typically fixed and does not change during training. SGD can have high 
        variance in the update steps, which can lead to slower convergence and oscillations around the minimum.

    Adam (Adaptive Moment Estimation):
        Adam is an extension of SGD that incorporates adaptive learning rates for each parameter.
        It computes adaptive learning rates for each parameter based on both the first-order momentum (like momentum in SGD) 
        and the second-order momentum (the moving average of squared gradients). This adaptive learning rate helps in adjusting 
        the learning rate for each parameter separately, leading to faster convergence and better performance. Adam is known to 
        work well in practice and has become a popular choice for training deep learning models.

In summary, while both SGD and Adam are optimization algorithms used for training AI models, Adam tends to converge faster and 
perform better in practice due to its adaptive learning rate approach. However, the performance comparison can vary depending on 
the specific dataset and model architecture, so it's always a good idea to try both and see which one works best for a particular 
task.
"""

try:
    # Asks training variables.
    naviText = "Navi> Would you like to know more about epochs and training models?"
    type_text(naviText)
    explanationChoice = input("\nYes or No: ").lower()

    if explanationChoice == "yes":
        type_text(epochExplain)
        epv = int(
            input("\nNavi> Now that we know what epochs are how many do you want to do: "))
        type_text(trainexplain)
        tmv = input(
            "\nNavi> Now that we know about SGD and Adam Which would you like to use? \nSGD or Adam: ").lower()
    if explanationChoice == "no":
        naviText = "\nNavi> Understood, lets get started then!\n"
        type_text(naviText)
        naviText = "\nNavi> How many epochs do you want to do: "
        type_text(naviText)
        naviChoice = input("")
        epv = int(naviChoice)
        naviText = "\nNavi> We can choose between the SGD and Adam training models \nWhich would you like to use: "
        type_text(naviText)
        naviChoice = input("").lower()
        tmv = naviChoice
    else:
        naviText = "\nNavi> That is not an option, try again next time!"
        type_text(naviText)

    naviText = "\nNavi> Lets plug this brain in and boot it up! Beginning training sequence now!\n"
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
    os.system("sudo rm ./training-data.json")
    os.system("sudo mv ./intenses_db/training-data.json training-data.txt")

    with open('training-data.txt', 'r') as f:
        file_contents = f.close()

    # Modify the file.
    with open('training-data.txt', 'r') as file:
        data = file.read()

    # Replace the target.
    data = data.replace(
        '        ]\n    },\n    {\n        "intents": [', '            ,')

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
    os.system("sudo mv ./training-data.txt ./training-data.json")

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
            words.extend(word_list)  # and adding them to words list

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
    tensorboard_callback = TensorBoard(
        log_dir='./tlogs', histogram_freq=1, write_graph=True, write_images=True)

    # Compiling the model.
    if tmv == "sgd":
        optimizer = SGD(learning_rate=0.001, decay=1e-6,
                        momentum=0.9, nesterov=True)
    if tmv == "adam":
        optimizer = Adam(learning_rate=0.001, decay=1e-6)

    model.compile(loss='categorical_crossentropy',
                  optimizer=tmv, metrics=['accuracy'])

    # Fit the model with TensorBoard callback
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=epv,
                     batch_size=5, verbose=1, callbacks=[tensorboard_callback])

    # Saves the model.
    model.save("echo.h5", hist)

    # Prints training complete and opens web panel.
    print(breakline)
    naviChoice = f"Navi> Oh wow {user}! I feel smarter... Do you wish to see the output of the training I just did?"
    type_text(naviChoice)
    tensorChoice = input("\nYes or No? ").lower()
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

    naviText = "\nNavi> Training complete! One last step before we finish up.\n"
    type_text(naviText)
except json.decoder.JSONDecodeError as e:
    print("\n[!] Error decoding JSON or training data:", e)
