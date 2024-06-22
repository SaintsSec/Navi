"""
Author: Alex Kollar | Project Manager: The Cryptex Project
Description: Binary translation for Cryptex
"""
from ..cipher import Cipher


class bin(Cipher):

    name = 'Binary Translator'
    type = 'datatype'

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = ' '.join(format(ord(x), 'b') for x in text)
        return {'text': output, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        binary_list = text.split(' ')
        output = ''
        for binary in binary_list:
            output += chr(int(binary, 2))
        return {'text': output, 'success': True}

    def print_options(self):
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
        total_tests = 2
        test_arg_list = ['bin', '--test', '-t', 'hello', '-k', '3']
        text_index = 3
        expect = '1101000 1100101 1101100 1101100 1101111'
        # NOTE (marvhus): Should the binary output have a byte length of 7 or 8?
        out = bin.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = bin.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total_tests} tests'}

