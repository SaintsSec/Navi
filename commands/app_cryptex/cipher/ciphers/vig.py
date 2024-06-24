"""
Author: @marvhus
Description: CryptexOOP Vignere Cipher ground up rewrite
"""
from ..cipher import Cipher
from itertools import cycle


class Vig(Cipher):
    name = 'Vignere Cipher'
    type = 'cipher'

    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        output = []
        for t, k in zip(text, cycle(key)):
            if t not in Vig.alphabet:
                output.append(t)
                continue
            t_index = Vig.alphabet.index(t)
            k_index = Vig.alphabet.index(k)
            x = (t_index + k_index) % 26
            output.append(Vig.alphabet[x])

        return {'text': "".join(output), 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")

        if not text:
            return {'text': "No input text", 'success': False}
        if not key:
            return {'text': "No key", 'success': False}

        output = []
        for t, k in zip(text, cycle(key)):
            if t not in Vig.alphabet:
                output.append(t)
                continue
            x = (ord(t) - ord(k) + 26) % 26
            x += ord('A')
            output.append(chr(x).lower())

        return {'text': "".join(output), 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -k / --key ------- key

        ### Examples
        python main.py text -e -t "hello" -k 'key'
        python main.py text -d -t "rijvs" -k 'key'
        ''')

    def test(args):
        test_total = 2
        test_arg_list = ['vig', '--test', '-t', 'hello', '-k', 'asd']
        text_index = 3

        expect = 'hwolg'
        out = Vig.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list[text_index], expect = expect, test_arg_list[text_index]
        out = Vig.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {test_total} tests'}
