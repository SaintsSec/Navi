"""
Author: @marvhus 
"""
from ..cipher import Cipher
import hashlib


class MD5(Cipher):  # make sure you change this from text to your cipher

    name = 'MD5'  # change the name
    type = 'hash function'

    @staticmethod
    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = hashlib.md5(text.encode).hexdigest()

        return {'text': output, 'success': True}

    @staticmethod
    def print_options(self):
        # Edit this section as needed for your specific encoding / decoding.
        print('''
        ### Modes
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py md5 -e -t 'hello'
        ''')
