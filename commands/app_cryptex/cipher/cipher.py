class Cipher(object):

    name = 'cipher'
    type = 'none'

    def encode(args):
        return {'text': 'Not implemented', 'success': False}

    def decode(args):
        return {'text': 'Not implemented', 'success': False}

    def print_options(self):
        print('''
        Not implemented.
        ''')

    def test(args):
        raise Exception('Not implemented')
        return {'status': False, 'msg': 'Not Implemented'}
