"""
Author: Alex Kollar | Project Manager: The Cryptex Project
Description: Base64 Cryptex implimentation
"""
import base64
from ..cipher import Cipher


class B64(Cipher):

    name = 'Base 64'
    type = 'cipher'

    @staticmethod
    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        text = text.encode('ascii')
        b64_bytes = base64.b64encode(text)
        output = b64_bytes.decode('ascii')
        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        try:
            b64_bytes = base64.b64decode(text)
            output = b64_bytes.decode('ascii')
            return {'text': output, 'success': True}
        except (base64.binascii.Error, ValueError) as e:
            return {'text': str(e), 'success': False}

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
        test_arg_list = ['b64', '--test', '-t', 'May Walla guide you! ', '-k', '3']
        text_index = 3
        test_arg_list[text_index] = 'hello'
        expect = 'aGVsbG8='
        out = B64.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode {test_arg_list[text_index]}
            expected "{test_arg_list[text_index]}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = B64.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode {test_arg_list[text_index]}
            expected "{test_arg_list[text_index]}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total_tests} tests'}
