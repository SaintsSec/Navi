from ..cipher import Cipher


class GC(Cipher):

    name = 'Gaderypoluki Cipher'
    type = 'cipher'

    def code(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")

        if not text:
            return {'text': "No input text", 'success': False}

        encode_lower = {
            'g': 'a',
            'a': 'g',
            'd': 'e',
            'e': 'd',
            'r': 'y',
            'y': 'r',
            'p': 'o',
            'o': 'p',
            'l': 'u',
            'u': 'l',
            'k': 'i',
            'i': 'k',
        }
        encode_upper = {
            'G': 'A',
            'A': 'G',
            'D': 'E',
            'E': 'D',
            'R': 'Y',
            'Y': 'R',
            'P': 'O',
            'O': 'P',
            'L': 'U',
            'U': 'L',
            'K': 'I',
            'I': 'K',
        }

        encode_text = ''

        for char in text:
            if char.isupper():
                char = encode_upper.get(char, char)
                encode_text += char
            elif char.islower():
                char = encode_lower.get(char, char)
                encode_text += char
            else:
                encode_text += char

        return {'text': encode_text, 'success': True}

    def encode(args):
        output = GC.code(args)
        return output

    def decode(args):
        output = GC.code(args)
        return output

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py gc -e -t 'hello'
        python main.py gc -d -t 'hduup'
        ''')
