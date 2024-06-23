"""
Author: @marvhus
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from ..cipher import Cipher


class R47(Cipher):
    name = 'Rot 47'
    type = 'cipher'

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = ''

        for character in text:
            encoded = ord(character)
            if 33 <= encoded <= 126:
                output += chr(33 + ((encoded + 14) % 94))
            else:
                output += character

        return {'text': output, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = ''

        for character in text:
            encoded = ord(character)
            if 33 <= encoded <= 126:
                output += chr(33 + ((encoded + 14) % 94))
            else:
                output += character

        return {'text': output, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py r47 -e -t 'hello'
        python main.py r47 -d -t 'hello'
        ''')

    def test(args):
        test_total = 2
        test_arg_list = ['r47', '--test', '-t', 'hello', '-k', '3']
        text_index = 3

        expect = '96==@'
        out = R47.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode {test_arg_list[text_index]}
            expected {test_arg_list[text_index]} got {out['text']}'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = R47.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode {test_arg_list[text_index]}
            expected {test_arg_list[text_index]} got {out['text']}'''}

        return {'status': True, 'msg': f'Ran {test_total} tests'}
