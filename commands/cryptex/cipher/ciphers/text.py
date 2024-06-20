from cipher import Cipher

class Text(Cipher):

    name = 'Plain text cipher'
    type = 'cipher'

    def encode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Do stuff with input

        return {'text': text, 'success': True}

    def decode(args):
        text = args.text

        if not text:
            return {'text': "No input text", 'success': False}

        # Do stuff with input

        return {'text': text, 'success': True}

    def print_options():
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text

        ### Example
        python main.py text -t 'hello'
        ''')

    def test(args):
        total = 2
        args.text = 'hello'
        out = Text.encode(args)
        if not out['success'] or args.text not in out['text']:
            return {'status': False, 'msg': f'''Failed to encode {args.text}
            expected {args.text} got {out['text']}'''}

        args.text = 'hello'
        out = Text.decode(args)
        if not out['success'] or args.text != out['text']:
            return {'status': False, 'msg': f'''Failed to decode {args.text}
            expected {args.text} got {out['text']}'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
        
