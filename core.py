import json 
import re 
import os
import modules.personality
from modules.mods import banner, bothelp, os
from modules.mods import clear

personality = modules.personality
clear()
print(banner)
def loadJson(file):
    with open(file) as personality:
        #print(f"Loaded {file} successfully!")
        return json.load(personality)

responsesData = loadJson('intents.json')

def getResponse(inputString):
    splitMessage = re.split(r'\s+|[,;?!.-]\s*', inputString.lower())
    scoreList = []

    for response in responsesData:
        responseScore = 0
        requiredScore = 0
        requiredWords = response['required_words']

        if requiredWords:
            for word in splitMessage:
                if word in requiredWords:
                    requiredScore += 1

        if requiredScore == len(requiredWords):
            for word in splitMessage:
                if word in response["user_input"]:
                    responseScore += 1

        scoreList.append(responseScore)

    bestResponse = max(scoreList)
    responseIndex = scoreList.index(bestResponse)

    if inputString == '':
        return "Please type something so we can chat :)"

    if bestResponse != 0:
        return responsesData[responseIndex]["bot_response"]

    return personality.idk()

while True:
    userInput = input(' > ')
    if userInput == "help":
        print("Navi: Here is the basic help information:")
        print(bothelp)
        continue
    elif userInput == 'cls':
        clear()
        continue
    elif userInput == 'cryptex':
        os.system('python3 ~/.Cryptex/src/main.py')
    elif userInput == "exit":
        print("Navi: It was fun talking to you, see yah soon!")
        exit()
    else:
        print(" Navi: ", getResponse(userInput))
