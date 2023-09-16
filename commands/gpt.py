import openai
from mods import mods
import random
import time
import datetime
import os

# Add your OpenAI API key here
openai.api_key = ""

# Add your GPT-3 engine here
command = "/gpt"
use = "Access GPT"
art = mods.gptArt


def typewriter(text):
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


def generate_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )
    if response.choices:
        return response.choices[0].text.strip()
    return ""


def run():
    print(art)
    prompt = input("Navi> [!] - Enter your prompt \n=> ")
    completion = generate_completion(prompt)
    print("Navi> ")
    typewriter(completion)
    # check if logs folder exists
    if not os.path.exists("logs/navi"):
        os.system("mkdir logs/navi")
    # check if log file exists
    if not os.path.exists("logs/navi/gpt.json"):
        os.system("touch logs/navi/gpt.json")
    # write to log file
    with open("logs/navi/gpt.json", "a") as f:
        now = datetime.datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        f.write(f"Date: {date_time}\n")
        f.write(f"Prompt: {prompt}\n")
        completion = "\n".join(completion[i:i+80]
                               for i in range(0, len(completion), 80))
        f.write(f"Completion: {completion}\n")
        f.write("\n")


if __name__ == "__main__":
    run()
