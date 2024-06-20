"""
Author: @marvhus
"""
from cipher import Cipher

class str2int(Cipher): #make sure you change this from text to your cipher

    name = 'str2int' #change the name
    type = 'cipher'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        out = 0

        for i, val in enumerate(text):
            char = ord(val)
            adjusted = char << i * 8
            out += adjusted

        return {'text': out, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        out = ""
        num = int(text)
        str_length = len(hex(num)[2:])//2

        for i in range(str_length):
            mask = 0xFF
            char = (num >> i * 8) & mask
            out += chr(char)

        return {'text': out, 'success': True}

    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py str2int -e -t 'hello'
        python main.py str2int -d -t ''
        ''')
