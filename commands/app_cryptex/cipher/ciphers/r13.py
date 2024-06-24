"""
Author: @marvhus
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from ..cipher import Cipher
from .cc import CC


class R13(Cipher):

    name = "Rot 13"
    type = 'cipher'

    def encode(args):
        from ....cryptex import get_argument_value, check_argument
        text = get_argument_value(args, "text")
        index, _ = check_argument(args, "key")
        index += 1
        if not text:
            return {'text': "No input text", 'success': False}
        modified_arg = args
        modified_arg[index] = 13

        return CC.encode(modified_arg)

    def decode(args):
        from ....cryptex import get_argument_value, check_argument
        text = get_argument_value(args, "text")
        index, _ = check_argument(args, "key")
        index += 1
        if not text:
            return {'text': "No input text", 'success': False}

        modified_arg = args
        modified_arg[index] = 13

        return CC.decode(modified_arg)

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py r13 -e -t 'hello'
        python main.py r13 -d -t 'hello'
        ''')

    def test(args):
        test_total = 2
        test_arg_list = ['r13', '--test', '-t', 'hello', '-k', '3']
        text_index = 3
        expect = 'uryyb'
        out = R13.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = R13.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {test_total} tests'}
