from ..cipher import Cipher


class CC(Cipher):
    name = 'Caesar Cipher'
    type = 'cipher'

    def encode(args):
        from ....cryptex import get_argument_value
        output = ''
        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")
        exclude_options = get_argument_value(args, "exclude")
        exclude = exclude_options if exclude_options else "\n\t .?!,/\\<>|[]{}@#$%^&*()-_=+`~:;\"'0123456789"
        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No shift key", 'success': False}

        for character in text:
            if character in exclude:
                output += character
            elif character.isupper():
                output += chr((ord(character) + int(key) - 65) % 26 + 65)
            else:
                output += chr((ord(character) + int(key) - 97) % 26 + 97)
        return {'text': output, 'success': True}

    def decode(args):
        from ....cryptex import get_argument_value
        output = ''

        text = get_argument_value(args, "text")
        key = get_argument_value(args, "key")
        exclude_options = get_argument_value(args, "exclude")
        exclude = exclude_options if exclude_options else "\n\t .?!,/\\<>|[]{}@#$%^&*()-_=+`~:;\"'0123456789"

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No shift key", 'success': False}

        for character in text:
            if character in exclude:
                output += character
            elif character.isupper():
                output += chr((ord(character) - int(key) - 65) % 26 + 65)
            else:
                output += chr((ord(character) - int(key) - 97) % 26 + 97)
        return {'text': output, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -k / --key ------- shift key
        -ex / --exclude -- exclude list

        ### Examples
        python main.py cc -e -t "hello" -k 10
        python main.py cc -d -t "hello" -k 10
        python main.py cc -e -t "hello" -k 10 -ex '123456789'
        python main.py cc -d -t "hello" -k 10 -ex '123456789'
       ''')

    def test(args):

        test_arg_list = ['cc', '--test', '-t', 'May Walla guide you! ', '-k', '3']
        text_index = 3
        key_index = 5

        total = 0
        expect = [
            'hello',
            'ifmmp',
            'jgnnq',
            'khoor',
            'lipps',
            'mjqqt',
            'nkrru',
            'olssv',
            'pmttw',
            'qnuux',
            'rovvy',
            'spwwz',
            'tqxxa',
            'uryyb',
            'vszzc',
            'wtaad',
            'xubbe',
            'yvccf',
            'zwddg',
            'axeeh',
            'byffi',
            'czggj',
            'dahhk',
            'ebiil',
            'fcjjm',
            'gdkkn',
            'hello',
        ]
        for i in range(1, 26):
            total += 1
            test_arg_list[text_index] = 'hello'
            test_arg_list[key_index] = i
            out = CC.encode(test_arg_list)
            if not out['success']:
                return {'status': False, 'msg': f'''
            Encoding failed: "{out['text']}"'''}

            if out['text'] not in expect[i]:
                return {'status': False, 'msg': f'''Failed to encode "hello"
                expected "{expect[i]}" with key {i} got {out['text']}'''}

        for i in range(1, 26):
            total += 1
            test_arg_list[text_index] = expect[i]
            test_arg_list[key_index] = i
            out = CC.decode(test_arg_list)
            if not out['success']:
                return {'status': False, 'msg': f'''
            Decoding failed: "{out['text']}"'''}

            if out['text'] not in 'hello':
                return {'status': False, 'msg': f'''Failed to decode "{expect[i]}"
                expected "hello" with key {i} got {out['text']}'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
