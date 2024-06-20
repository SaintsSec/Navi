"""
Author: @marvhus
"""
from ..cipher import Cipher


class Oct(Cipher): # make sure you change this from text to your cipher

    name = 'Octal' # change the name
    type = 'cipher'

    @staticmethod
    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = " ".join(oct(ord(char))[2:] for char in text)

        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = "".join(chr(int(char, base = 8)) for char in text.split(' '))

        return {'text': output, 'success': True}

    @staticmethod
    def print_options(self):
        # Edit this section as needed for your specific encoding / decoding.
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py oct -e -t 'hello'
        python main.py oct -d -t '150 145 154 154 157'
        ''')

    def test(args):
        total = 2

        args.text = 'hello'
        expect = '150 145 154 154 157'
        out = Oct.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = Oct.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
