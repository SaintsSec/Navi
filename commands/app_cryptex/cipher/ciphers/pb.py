from ..cipher import Cipher
import itertools


class Pb(Cipher):
    name = 'Pb'
    type = 'cipher'

    def brute(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text").strip().replace('"', '').replace("'", '')
        range_split = [i.strip() for i in get_argument_value(args, "range").split(',') if i.strip()]
        range_int = [int(i) for i in range_split if i.isdigit()]
        step = 1

        # Validate if correct input
        if not text:
            return {'text': "No input text", 'success': False}
        if not text.isdigit():
            return {'text': "Input Text should only contain digits", 'success': False}

        # Validate Range
        if not range_int or len(range_int) != len(range_split):
            return {'text': "Improper Range", 'success': False}

        if len(range_int) < 2:
            range_int.append(range_int[0] + step)

        digits = [f"{i}" for i in range(10)]

        for length in range(range_int[0], range_int[1], step):
            for item in itertools.product(digits, repeat=length):
                guess = "".join(item)
                if guess == text:
                    return {'text': "Found the pin", 'success': True}

        return {'text': "Couldn't find the pin", 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -b / --brute ---- brute
        ### Input
        -t / --text ------ input text
        -i / --input ------ input file [.txt]
        -r / --range ------- range [<start>, <end> or <start>]
        ### Examples
        python main.py pb -b -t '1234' -r 4
        python main.py pb -b -t '1234' -r 3,5
        python main.py pb -b -i <path_to_.txt> -r 2,3
        ''')
