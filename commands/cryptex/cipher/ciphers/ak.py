from cipher import Cipher

class AK(Cipher):

    name = 'Autokey Cipher'
    type = 'cipher'

    def encode(args):
        output = ''
        text = args.text.lower()
        key = args.key
        exclude = args.exclude if args.exclude else "\n\t .?!,/\\<>|[]{}@#$%^&*()-_=+`~:;\"'0123456789"
        new_key = ''
        temp =  key + text

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No shift key", 'success': False}

        for k in temp:
            if k not in exclude:
                new_key += k

        output = []
        i = 0
        for c in text:
            if c in exclude:
                output.append(c)
            else:
                x = ((ord(c) % 97) + (ord(new_key[i]) % 97)) % 26  
                x += ord('a')
                i += 1
                output.append(chr(x))

        return {'text': "".join(output), 'success': True}

    def decode(args):
        output = ''
        text = args.text
        key = args.key
        exclude = args.exclude if args.exclude else "\n\t .?!,/\\<>|[]{}@#$%^&*()-_=+`~:;\"'0123456789"
        new_key = ''

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No shift key", 'success': False}

        for k in key:
            if k not in exclude:
                new_key += k

        output = []
        i = 0
        for c in text:
            if c in exclude:
                output.append(c)
            else:
                x = ((ord(c) % 97) - (ord(new_key[i]) % 97)) % 26  
                x += ord('a')
                output.append(chr(x))
                new_key += chr(x)
                i += 1

        return {'text': "".join(output), 'success': True}


    def print_options():
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
