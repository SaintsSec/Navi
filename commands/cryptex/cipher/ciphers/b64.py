"""
Author: Alex Kollar | Project Manager: The Cryptex Project
Description: Base64 Cryptex implimentation
"""
from ..cipher import Cipher
import base64


class B64(Cipher): #make sure you change this from text to your cipher

    name = 'Base 64' #change the name
    type = 'cipher'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Here is where you put your encoding / encrypting code.
        text = args.text.encode('ascii')
        b64_bytes = base64.b64encode(text)
        output = b64_bytes.decode('ascii')
        return {'text': output, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        #Here is where you put your decoding / decrypting code.
        text = args.text.encode('ascii')
        b64_bytes = base64.b64decode(text)
        output = b64_bytes.decode('ascii')
        return {'text': output, 'success': True}

    def print_options(self):
        # Edit this section as needed for your specific encoding / decoding.
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
        total = 2

        args.text = 'hello'
        expect = 'aGVsbG8='
        out = B64.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode {args.text}
            expected "{args.text}" got "{out['text']}"'''}

        args.text, expect = expect, args.text
        out = B64.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode {args.text}
            expected "{args.text}" got "{out['text']}"'''}
        
        return {'status': True, 'msg': f'Ran {total} tests'} 
