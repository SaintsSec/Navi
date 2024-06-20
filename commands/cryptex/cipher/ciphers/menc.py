from cipher import Cipher

class Menc(Cipher):

    name = 'Menc'
    type = 'cipher'

    def encode(args):
        text = args.text
        outputs = args.key
        alphabet = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

        if not text:
            return {'text': "No input text", 'success': False}

        if not outputs:
            return {'text': "No output text", 'success': False}

        inputList = []
        for char in text:
            index = alphabet.index(char)
            if index == -1:
                return {'text': "Invalid character in input text", 'success': False}
            inputList.append(index)

        outputList = []
        for char in outputs:
            index = alphabet.index(char)
            if index == -1:
                return {'text': "Invalid character in key", 'success': False}
            outputList.append(index)

        key = ""
        for index, value in enumerate(inputList):
            outputCharIndex = outputList[index % len(outputList)]

            if value == outputCharIndex:
                difference = 0
            elif value < outputCharIndex:
                difference = outputCharIndex - value
            else :
                difference = len(alphabet) - (value - outputCharIndex)

            if outputCharIndex != (value + difference) % len(alphabet):
                return {'text': "Error, could not find the charIndex difference", 'success': False}

            key += "%0.2X" % difference
        return {'text': key, 'success': True}


    def decode(args):
        text = args.text
        key = args.key
        alphabet = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

        if not text:
            return {'text': "No input text", 'success': False}

        if not key:
            return {'text': "No key", 'success': False}

        if len(key) % 2 != 0:
            return {'text': "Invalid key", 'success': False}

        keyList = [key[i:i+2] for i in range(0, len(key), 2)]
        for index, value in enumerate(keyList):
            keyList[index] = int(value, 16)

        encryptedList = []
        for char in text:
            index = alphabet.index(char)
            if index == -1:
                return {'text': "Invalid character in input text", 'success': False}
            encryptedList.append(index)

        decrypted = ""
        for index in range(len(keyList)):
            charIndex = (encryptedList[index % len(encryptedList)] - keyList[index]) % len(alphabet)
            decrypted += alphabet[charIndex]

        return {'text': decrypted, 'success': True}

    def print_options():
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
