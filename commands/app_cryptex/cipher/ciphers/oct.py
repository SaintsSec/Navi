"""
Author: @marvhus
"""
from ..cipher import Cipher


class Oct(Cipher): # make sure you change this from text to your cipher

    name = 'Octal' # change the name
    type = 'cipher'

    @staticmethod
    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = " ".join(oct(ord(char))[2:] for char in text)

        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = "".join(chr(int(char, base = 8)) for char in text.split(' '))

        return {'text': output, 'success': True}

    @staticmethod
    def print_options(self):
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
        test_total = 2
        test_arg_list = ['oct', '--test', '-t', 'hello', '-k', '3']
        text_index = 3

        expect = '150 145 154 154 157'
        out = Oct.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = Oct.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {test_total} tests'}
