"""
Author: Alex Kollar | Project Manager: The Cryptex Project
Description: A basic hexadecimal encoder / decoder
"""
#TODO Work an getting file output working.
from ..cipher import Cipher


class Hex(Cipher):

    name = 'Hex Encoder / Decoder'
    type = 'datatype'

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        # encode to hex
        output = text.encode("utf-8").hex()
        return {'text': output, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text").replace('"', '').replace("'", '')

        if not text:
            return {'text': "No input text", 'success': False}

        output = bytes.fromhex(text).decode("utf-8")
        return {'text': output, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Example
        python3 main.py -e -t 'Hello world!'
        ''')
        #TODO(marvhus): Remove -o/--output and instead implement it in the Main.output() function

    def test(args):
        total_tests = 2
        test_arg_list = ['hex', '--test', '-t', 'hello', '-k', '3']
        text_index = 3
        expect = '68656c6c6f'
        out = Hex.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index] = expect
        expect = 'hello'
        out = Hex.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total_tests} tests'}
