"""
Author: @marvhus
Description: CryptexOOP Vignere Cipher ground up rewrite
"""
from ..cipher import Cipher
from itertools import cycle


class Vig(Cipher):

    name = 'Vignere Cipher'
    type = 'cipher'

    alphabet = [chr(i).upper() for i in range(ord('a'), ord('z')+1)]

    def encode(args):
        text = args.text.upper()
        key = args.key.upper()

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        output = []
        for t,k in zip(text, cycle(key)):
            if t not in Vig.alphabet:
                output.append(t)
                continue
            x = ( ord(t) + ord(k) ) % 26
            x += ord('A')
            output.append( chr(x).lower() )

        return {'text': "".join(output), 'success': True}

    def decode(args):
        text = args.text.upper()
        key = args.key.upper()

        if not text:
            return {'text': "No input text", 'success': False}
        if not key:
            return {'text': "No key", 'success': False}

        output = []
        for t,k in zip(text, cycle(key)):
            if t not in Vig.alphabet:
                output.append(t)
                continue
            x = ( ord(t) - ord(k) + 26 ) % 26
            x += ord('A')
            output.append( chr(x).lower() )

        return {'text': "".join(output), 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -k / --key ------- key

        ### Examples
        python main.py text -e -t "hello" -k 'key'
        python main.py text -d -t "rijvs" -k 'key'
        ''') 

    def test(args):
        total = 2

        args.text = 'hello'
        args.key = 'asd'
        expect = 'hwolg'
        out = Vig.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = Vig.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
