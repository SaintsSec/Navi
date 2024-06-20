"""
Author: @marvhus
Description: Reverse Cipher Cryptex Implementation
"""
from cipher import Cipher

class RC(Cipher):

    name = 'Reverse cipher'
    type = 'cipher'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = text[::-1]

        return {'text': output, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = text[::-1]

        return {'text': output, 'success': True}
    
    def print_options():
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py rc -e -t 'hello'
        python main.py rc -d -t 'hello'
        ''')

    def test(args):
        total = 2

        args.text = 'hello'
        expect = 'olleh'
        out = RC.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode {args.text}
            expected {args.text} got {out['text']}'''}

        args.text, expect = expect, args.text
        out = RC.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode {args.text}
            expected {args.text} got {out['text']}'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
