"""
Author: @marvhus
Instructions:
    Rename the "Text" class to whatever cipher you are working on.
    Edit the encode and decode defs as required to encode or decode your cipher.
    make sure you add the following to __init__.py: from cipherfile import *
    Doing this will link the code to main.py 
"""
from cipher import Cipher

class Mor(Cipher): #make sure you change this from text to your cipher

    name = 'Morse code' #change the name
    type = 'cipher'

    morse_alphabet = {
        # Letters
        "A" : ".-",
        "B" : "-...",
        "C" : "-.-.",
        "D" : "-..",
        "E" : ".",
        "F" : "..-.",
        "G" : "--.",
        "H" : "....",
        "I" : "..",
        "J" : ".---",
        "K" : "-.-",
        "L" : ".-..",
        "M" : "--",
        "N" : "-.",
        "O" : "---",
        "P" : ".--.",
        "Q" : "--.-",
        "R" : ".-.",
        "S" : "...",
        "T" : "-",
        "U" : "..-",
        "V" : "...-",
        "W" : ".--",
        "X" : "-..-",
        "Y" : "-.--",
        "Z" : "--..",
        # Numbers
        "0" : "-----",
        "1" : ".----",
        "2" : "..---",
        "3" : "...--",
        "4" : "....-",
        "5" : ".....",
        "6" : "-....",
        "7" : "--...",
        "8" : "---..",
        "9" : "----.",
        # Punctuation
        "." : ".-.-.-",
        "," : "--..--",
        "?" : "..--..",
        "'" : ".----.",
        "!" : "-.-.--",
        "/" : "-..-.",
        "(" : "-.--.",
        ")" : "-.--.-",
        "&" : ".-...",
        ":" : "---...",
        ";" : "-.-.-.",
        "=" : "-...-",
        "+" : ".-.-.",
        "-" : "-....-",
        "_" : "..--.-",
        '"' : ".-..-.",
        "$" : "...-..-",
        "@" : ".--.-.",
        # non-Latin extensions
        # todo: add non-Latin stuff
        # space
        " " : "/" # custom seperator to make it easier to read
    }
    # https://en.wikipedia.org/wiki/Morse_code#Mnemonics

    inverse_morse_alphabet = dict((var, key) for (key, var) in morse_alphabet.items())

    get_dict_var = lambda dict, char : char if not char in dict else dict[char] 

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        output = []

        for char in text:
            output.append( Mor.get_dict_var(Mor.morse_alphabet, char.upper()) )

        return {'text': " ".join(output), 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        text = text.split(' ')

        output = ''
        for char in text:
            output += Mor.get_dict_var(Mor.inverse_morse_alphabet, char)

        return {'text': output, 'success': True}

    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Examples
        python main.py mor -e -t 'hello'
        python main.py mor -d -t '.... . .-.. .-.. ---'
        ''') 

    def test(args):
        total = 2

        args.text = 'HELLO'
        expect = '.... . .-.. .-.. ---'
        out = Mor.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = Mor.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
            
