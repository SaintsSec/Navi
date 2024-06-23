"""
Author: @marvhus
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from ..cipher import Cipher


class XOR(Cipher):
    name = 'XOR (Exclusive Or) Cipher'
    type = 'cipher'

    def str_xor(text, key):
        from itertools import cycle
        output = ''.join(
            chr(ord(c) ^ ord(k))
            for c, k in zip(text, cycle(key))
        )

        return output

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        output = XOR.str_xor(text, key)

        return {'text': output, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        output = XOR.str_xor(text, key)

        return {'text': output, 'success': True}

    def print_options(self):
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
        test_total = 2
        test_arg_list = ['xor', '--test', '-t', 'HELLO', '-k', 'asd']
        text_index = 3
        expect = ')6(-<'
        out = XOR.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = XOR.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {test_total} tests'}
