"""
Author: @Iqrar99, @kailashchoudhary11
Description: A basic Baconian Chiper encoder / decoder
"""
from ..cipher import Cipher


class Bac(Cipher):
    """
    This chiper uses 26 alphabets version.
    """
    name = 'Baconian Chiper'
    type = 'cipher'

    def encode(args):
        from ....cryptex import get_argument_value
        ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        char1 = 'a'
        char2 = 'b'

        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")

        if not text:
            return {'text': "No input text", 'success': False}

        if key:
            if len(key) == 1 or len(key) > 2:
                return {'text': "Key must be 2 characters", 'success': False}
            elif len(key) == 2:
                char1 = key[0]
                char2 = key[-1]
                if char1 == char2:
                    return {'text': f"Key '{char1}' and '{char2}' can't be similar", 'success': False}

        # Ignore non-alphabetic characters
        text_split = [c.upper() for c in text if c.isalpha()]

        # Make a bacon code
        bacon_list = []
        bin_cnt = 0
        for c in ALPHABET:
            bacon_list.append([c, bin(bin_cnt)[2:].zfill(5)])
            bin_cnt += 1
        bacon_idx =  dict(bacon_list)

        # Convert the alphabet into bacon code
        for i in range(len(text_split)):
            bin_representation = bacon_idx[text_split[i]]
            text_split[i] = bin_representation.replace('0', char1).replace('1', char2)

        encoded_text = ''.join(text_split)

        return {'text': encoded_text, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        use_default_key = True
        char1 = 'A'  # Default key
        char2 = 'B'  # Default key

        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")

        if not text:
            return {'text': "No input text", 'success': False}
        else:
            text = text.upper()

        if key is not None and len(key) != 0:
            if len(key) != 2:
                return {'text': "Key must be 2 characters", 'success': False}
            else:
                use_default_key = False
                key = key.upper()
                char1, char2 = key
                if char1 == char2:
                    return {'text': f"Key '{char1}' and '{char2}' can't be similar", 'success': False}
        else:
            key = char1+char2

        # Check if the characters are valid with the key
        clean_text = []
        for c in text:
            # Ignore non-alphabetic characters
            if c.isalpha() and c in key:
                clean_text.append(c)
            elif not c.isalpha():
                continue
            else:
                return {
                    'text': f"Key '{key if use_default_key else args.key}' and encoded text '{args.text}' is not matched",
                    'success': False
                }

        text = ''.join(clean_text)

        if len(text) % 5:
            return {
                'text': "The encoded text must be a length in multiples of 5",
                'success': False
            }

        # Make a bacon code
        bacon_list = []
        bin_cnt = 0
        for c in ALPHABET:
            bacon_list.append([bin(bin_cnt)[2:].zfill(5), c])
            bin_cnt += 1
        bacon_idx_reversed = dict(bacon_list)

        # group the encoded text into 5 characters each
        grouped_text = []
        for mul in range(len(text)//5):
            grouped_text.append(text[mul*5:(mul+1)*5])

        # Convert the bacon code into alphabet
        for i in range(len(grouped_text)):
            alpha_representation = grouped_text[i].replace(char1, '0').replace(char2, '1')
            try:
                grouped_text[i] = bacon_idx_reversed[alpha_representation]
            except KeyError:
                return {
                    'text': f"'{grouped_text[i]}' can't be recognized by the Bacon Index because it contains a binary that more than 10111",
                    'success': False
                }

        decoded_text = ''.join(grouped_text)

        return {'text': decoded_text, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text. Only accept alphabetic characters. Outside of it will be ignored.
        -k / --key ------ key contains 2 characters only

        ### Examples
        python main.py bac -e -t 'hello'
        python main.py bac -d -t 'aabbbabaaa'
        python main.py bac -e -t 'hello' -k 'xy'
        python main.py bac -d -t 'xxyyyxyxxx' -k 'xy'
        ''')
