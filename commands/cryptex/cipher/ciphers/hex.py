"""
Author: Alex Kollar | Project Manager: The Cryptex Project
Description: A basic hexadecimal encoder / decoder
"""
#TODO Work an getting file output working.
from cipher import Cipher

class Hex(Cipher): #make sure you change this from text to your cipher

    name = 'Hex Encoder / Decoder' #change the name
    type = 'datatype'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Here is where you put your encoding / encrypting code.
        # encode to hex
        output = text.encode("utf-8").hex()
        return {'text': output, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        #Here is where you put your decoding / decrypting code.
        output = bytes.fromhex(text).decode("utf-8")
        return {'text': output, 'success': True}

    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
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
        total = 2

        args.text = 'hello'
        expect = '68656c6c6f'
        out = Hex.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text = expect
        expect = 'hello'
        out = Hex.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
        
