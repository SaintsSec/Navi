"""
Author: Sparsh Gupta | Contributor
Description: Affine Cipher Implementation
"""
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

class Affine(Cipher): #make sure you change this from text to your cipher

    name = 'Affine' #change the name
    type = 'cipher'


    def encode(args):
        text = args.text
        key_a=args.key_a
        key_b=args.key_b

        if not text:
            return {'text': "No input text", 'success': False}

        if key_a==None :
            key_a=1
        if key_b==None:
            key_b=0

        
        default_dict='abcdefghijklmnopqrstuvwxyz'
        m=len(default_dict)

        output=''
        for char in text:
            if(char in default_dict):
                x=default_dict.find(char)
                e_x=(key_a*x+key_b)%m
                output+=default_dict[e_x]
            else:
                output+=char
        return {'text': output, 'success': True}

    def decode(args):
        text = args.text
        key_a=args.key_a
        key_b=args.key_b

        if not text:
            return {'text': "No input text", 'success': False}

        if key_a==None :
            key_a=1
        if key_b==None:
            key_b=0

        
        default_dict='abcdefghijklmnopqrstuvwxyz'
        m=len(default_dict)

        output=''
        for char in text:
            if(char in default_dict):
                x=default_dict.find(char)
                e_x=(mod_inv(key_a,m)*((x-key_b)%m))%m
                output+=default_dict[e_x]
            else:
                output+=char
        return {'text': output, 'success': True}


    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -ka / --key_a ------input key -a
        -kb / --key_b -------input key -b

        ### Examples
        python main.py text -e -t 'hello' -ka 21 -kb 1
        python main.py text -d -t 'hello' -ka 2

        Note: Cipher is Case Sensitive. Default Dictionary: abcdefghijklmnopqrstuvwxyz
        ''')
