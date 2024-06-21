"""
Author: @marvhus
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from ..cipher import Cipher
from .cc import CC


class R13(Cipher):

    name = "Rot 13"
    type = 'cipher'

    def encode(args):
        if not args.text:
            return {'text': "No input text", 'success': False}

        args.key = 13

        return CC.encode(args)

    def decode(args):
        if not args.text:
            return {'text': "No input text", 'success': False}

        args.key = 13

        return CC.decode(args)

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py r13 -e -t 'hello'
        python main.py r13 -d -t 'hello'
        ''')

    def test(args):
        total = 2

        args.text = 'hello'
        expect = 'uryyb'
        out = R13.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = R13.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
