"""
Author: @oriapp 
"""
from ..cipher import Cipher
import hashlib


class sha384(Cipher):

    name = 'sha384'
    type = 'hash function'

    @staticmethod
    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = hashlib.sha384(text.encode()).hexdigest()

        return {'text': output, 'success': True}

    @staticmethod
    def print_options(self):
        print('''
        ### Modes
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py sha384 -e -t 'hello'
        ''')
