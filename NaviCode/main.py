import openai, os, subprocess, time
from mods import mods


# [!!] - YOU WILL NEED TO ADD YOUR OWN GPT API KEY HERE!!
openai.api_key = "YOU WILL NEED TO ADD YOUR OWN GPT API KEY HERE!!"
# [!!] - HEY LOOK TWO LINES UP AND READ TO HERE JUST IN CASE...

art = mods.art
breakline = mods.breakline
clearScreen = mods.clearScreen

#Clears the screen and prints out the header
clearScreen
print(art)

#Main loop for gpt / commands
while True:
    #Main input 
    chatText = input("Navi> Whats up? \n")
    #Looking out for / commands 
    if chatText == "/stop":
        print(breakline)
        print("Navi> [!!] - I look forward to seeing you again!")
        print(breakline)
        time.sleep(3)
        clearScreen
        break
    if chatText == "/recon":
        print(breakline)
        print("Navi> [!!] - Launching recon automation RIGHT NOW!!")
        print(breakline)
        time.sleep(3)
        subprocess.call(['python3', './recon.py'])
        break
    if chatText == "/clear":
        print(breakline)
        print("Navi> [!!] - Rebooting, see you in a second!")
        print(breakline)
        time.sleep(3)
        subprocess.call(['python3', './main.py'])
        break
    if chatText == "/help":
        subprocess.call(['python3', './help.py'])
        break
    #Generate AI response if /command not present 
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = chatText,
        temperature = 0.7,
        max_tokens = 256,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    #Prints out AI response.
    print(response["choices"][0]["text"])
    print(breakline)
