
"""
Author: @marvhus
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from cipher import Cipher

class XOR(Cipher): #make sure you change this from text to your cipher

    name = 'XOR (Exclusive Or) Cipher' #change the name
    type = 'cipher'

    def str_xor(text, key):
        from itertools import cycle
        output = ''.join(
            chr(ord(c) ^ ord(k))
            for c,k in zip(text, cycle(key))
        )

        return output


    def encode(args):
        text = args.text
        key = args.key

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        output = XOR.str_xor(text, key)

        return {'text': output, 'success': True}

    def decode(args):
        text = args.text
        key = args.key

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        output = XOR.str_xor(text, key)

        return {'text': output, 'success': True}

    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -k / --key ------- key

        ### Examples
        python main.py text -e -t 'hello' -k 'KEY'
        python main.py text -d -t '# 5'*' -k 'KEY'
        ''')

    def test(args):
        total = 2

        args.text = 'HELLO'
        args.key = 'asd'
        expect = ')6(-<'
        out = XOR.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = XOR.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}
        
        return {'status': True, 'msg': f'Ran {total} tests'}
