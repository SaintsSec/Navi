
class MenuSystem:
    def __init__(self, cipher_list):
        self.sort_ciphers(cipher_list)

    # sort the ciphers by type
    def sort_ciphers(self, cipher_list):
        self.types = {}

        for cipher in cipher_list:
            if cipher.type in self.types:
                self.types[cipher.type] = []
            self.types[cipher.type].append(cipher)

        print(self.types)
