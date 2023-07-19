import time
import random
import sys

def typewriter(text):
    for char in text: 
        print(char, end="", flush=True,)
        # generate a random number between 0 and 1
        random_num = random.random()
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