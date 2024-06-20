from cipher import Cipher
import math

def extended_euclidean_common_devisor(a, b): 
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_euclidean_common_devisor(b % a, a)
        return (gcd, y - (b // a) * x, x)


def mod_inv(a, m):
    gcd, x, _ = extended_euclidean_common_devisor(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

class MC(Cipher):
    
    name = 'Multiplicative Cipher'
    type = 'cipher'

    def encode(args):
        lookup_table={}
        for i in range(26):
            lookup_table[chr(ord('a') + i)] = i
            lookup_table[chr(ord('A') + i)] = 26 + i
        key_list = list(lookup_table.keys())
        inv_lookup_table = dict(zip(lookup_table.values(), lookup_table.keys()))

        output = ''
        text = args.text
        try:
            key = int(args.key)
        except ValueError:
            return {'text': "Key has to be a whole number", 'success': False}

        if not text:
            return {'text': "No input text", 'success': False}

        if math.gcd(26, key) == 1:
            for char in text:
                if char in key_list:
                    offset = 0 if char.islower() else 26
                    new_index = (lookup_table[char] * key) % 26
                    output += inv_lookup_table[new_index + offset]
                else:
                    output += char
        else:
            return {'text': "Key is not co-prime to 26", 'success': False}

        return {'text': output, 'success': True}

    def decode(args):
        lookup_table = {}
        for i in range(26):
            lookup_table[chr(ord('a') + i)] = i
        key_list = list(lookup_table.keys())
        inv_lookup_table = dict(zip(lookup_table.values(), lookup_table.keys()))

        output = ''
        text = args.text
        key = args.key

        if not text:
            return {'text': "No input text", 'success': False}

        multi_inv = mod_inv(key, 26)
        for char in text:
            if char in key_list:
                new_index = (lookup_table[char.lower()] * multi_inv) % 26
                output += inv_lookup_table[new_index]
            else:
                output += char
        return {'text': output, 'success': True}

    def print_options():
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -k / --key ------- shift key
        ''')
