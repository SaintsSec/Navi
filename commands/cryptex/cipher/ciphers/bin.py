"""
Author: Alex Kollar | Project Manager: The Cryptex Project
Description: Binary translation for Cryptex
"""
from cipher import Cipher

class bin(Cipher): #make sure you change this from text to your cipher

    name = 'Binary Translator' #change the name
    type = 'datatype'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Here is where you put your encoding / encrypting code.
        output = ' '.join(format(ord(x), 'b') for x in text)
        return {'text': output, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        #Here is where you put your decoding / decrypting code.
        binary_list = text.split(' ')
        output = ''
        for binary in binary_list:
            output += chr(int(binary, 2))
        return {'text': output, 'success': True}

    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
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

    def test(args):
        total = 2

        args.text = 'hello'
        expect = '1101000 1100101 1101100 1101100 1101111'
        # NOTE (marvhus): Should the binary output have a byte length of 7 or 8?
        out = bin.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = bin.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
            
