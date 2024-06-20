"""
Author: @marvhus | Edits: Alex
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from ..cipher import Cipher


class Template(Cipher):

    name = 'Plain text cipher' 
    type = 'template'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Here is where you put your encoding / encrypting code.

        return {'text': text, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Here is where you put your decoding / decrypting code.

        return {'text': text, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py text -e -t 'hello'
        python main.py text -d -t 'hello'
        ''')
