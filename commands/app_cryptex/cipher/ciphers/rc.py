"""
Author: @marvhus
Description: Reverse Cipher Cryptex Implementation
"""
from ..cipher import Cipher


class RC(Cipher):

    name = 'Reverse cipher'
    type = 'cipher'

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = text[::-1]

        return {'text': output, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        output = text[::-1]

        return {'text': output, 'success': True}

    def print_options(self):
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
        test_total = 2

        test_arg_list = ['r47', '--test', '-t', 'hello', '-k', '3']
        text_index = 3

        expect = 'olleh'
        out = RC.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode {test_arg_list[text_index]}
            expected {args.text} got {out['text']}'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = RC.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode {test_arg_list[text_index]}
            expected {test_arg_list[text_index]} got {out['text']}'''}

        return {'status': True, 'msg': f'Ran {test_total} tests'}
