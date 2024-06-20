"""
Author: @marvhus 
"""
from cipher import Cipher
import string
import random

class PSWD(Cipher): #make sure you change this from text to your cipher

    name = 'Password generator' #change the name
    type = 'tool'

    @staticmethod
    def encode(args):
        len = args.length

        if not len:
            return {'text': "No password length", 'success': False}

        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

        ## shuffling the characters
        random.shuffle(characters)
	
    	## picking random characters from the list
        password = []
        for _ in range(len):
            password.append(random.choice(characters))

	    ## shuffling the resultant password
        random.shuffle(password)

        return {'text': "".join(password), 'success': True}

    @staticmethod
    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -e / --encode ---- encode

        ### Input
        -len ------------- input text

        ### Examples
        python main.py pswd -e -len 32
        ''')
