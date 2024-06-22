from ..cipher import Cipher


class Menc(Cipher):
    name = 'Menc'
    type = 'cipher'

    def encode(args):
        text = args.text
        outputs = args.key
        alphabet = r" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

        if not text:
            return {'text': "No input text", 'success': False}

        if not outputs:
            return {'text': "No output text", 'success': False}

        input_list = []
        for char in text:
            index = self.alphabet.index(char)
            if index == -1:
                return {'text': "Invalid character in input text", 'success': False}
            input_list.append(index)

        output_list = []
        for char in outputs:
            index = alphabet.index(char)
            if index == -1:
                return {'text': "Invalid character in key", 'success': False}
            output_list.append(index)

        key = ""
        for index, value in enumerate(input_list):
            output_char_index = output_list[index % len(output_list)]

            if value == output_char_index:
                difference = 0
            elif value < output_char_index:
                difference = output_char_index - value
            else:
                difference = len(alphabet) - (value - output_char_index)

            if output_char_index != (value + difference) % len(alphabet):
                return {'text': "Error, could not find the char_index difference", 'success': False}

            key += "%0.2X" % difference
        return {'text': key, 'success': True}

    def decode(args):
        text = args.text
        key = args.key
        alphabet = r" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        if len(key) % 2 != 0:
            return {'text': "Invalid key", 'success': False}

        key_list = [key[i:i + 2] for i in range(0, len(key), 2)]
        for index, value in enumerate(key_list):
            key_list[index] = int(value, 16)

        encrypted_list = []
        for char in text:
            index = alphabet.index(char)
            if index == -1:
                return {'text': "Invalid character in input text", 'success': False}
            encrypted_list.append(index)

        decrypted = ""
        for index in range(len(key_list)):
            char_index = (encrypted_list[index % len(encrypted_list)] - key_list[index]) % len(alphabet)
            decrypted += alphabet[char_index]

        return {'text': decrypted, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -e / --encode ---- encode
        -d / --decode ---- decode

        ### Input
        -t / --text ------ input text
        -k / --key ------- key

        ### Examples
        python main.py menc -e -t 'hello' -k 'world'

        python main.py menc -d -t 'world' -k '0F0A060054'
        ''')
