"""
Author: @marvhus
"""
from ..cipher import Cipher


class L33T(Cipher):  # make sure you change this from text to your cipher

    name = 'L33t Sp34k'  # change the name
    type = 'cipher'

    leet_speak = {
        'a': '4',
        'b': '8',
        'c': '(',
        'e': '3',
        'g': '6',
        'h': 'H',
        'i': '1',
        'k': 'X',
        'l': 'l',
        'o': '0',
        'p': '9',
        's': '5',
        't': '7',
        'x': '*',
        'z': '2',
    }
    inverse_leet_speak = dict((v, k) for k, v in leet_speak.items())

    convertWithDict = lambda dict, char: dict[char] if char in dict else char

    @staticmethod
    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text").lower()

        if not text:
            return {'text': "No input text", 'success': False}

        output = ''.join(L33T.convertWithDict(L33T.leet_speak, char) for char in text)

        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = ''.join(L33T.convertWithDict(L33T.inverse_leet_speak, char) for char in text)

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
        python main.py l33t -e -t 'hello'
        python main.py l33t -d -t 'h3llo'
        ''')

    def test(args):
        total_tests = 2
        test_arg_list = ['hex', '--test', '-t', 'hello', '-k', '3']
        text_index = 3
        
        expect = 'H3ll0'
        out = L33T.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = L33T.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total_tests} tests'}
