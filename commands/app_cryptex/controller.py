import argparse
import itertools
import sys
from typing import List

from colorama import Fore

from navi_shell import tr
from .vars import banner


class CLIManager:
    def __init__(self, cipher_list):
        self.cipher_list = cipher_list
        self.cipher_types = {}
        self.line = self.__add_extra("", 37, "-")

    def __add_extra(self, str, max, char):
        amount = max - len(str)
        if amount <= 0:
            str = str[: amount - 1]
            return str
        str = str + char * amount
        return str

    def print_ciphers(self):
        # loop over all the ciphers
        for name in self.cipher_list:
            # get the cipher type
            type = self.cipher_list[name].type
            # check if type is in dict, if not then add it
            if not type in self.cipher_types:
                self.cipher_types[type] = []
            # add cipher long name and short name to list of that ciphers type
            self.cipher_types[type].append([self.cipher_list[name].name, name])

        # print cryptex banner
        banner()

        # Printing magic
        for key in self.cipher_types:
            print("|" + self.__add_extra(f"-- {key}s", len(self.line), "-") + "|-- short name ------|")
            for item in self.cipher_types[key]:
                print("|      " + self.__add_extra(item[0], 30, " ") + f" |      {item[1]} \t   |")
        print("|" + self.line + "|" + self.__add_extra("", 20, "-") + "|")

    def print_output(self, output: str, args: argparse.Namespace):
        from ..cryptex import check_argument
        if "languages" in output:
            return

        if not output["success"]:
            sys.exit(f'Failed to run cipher "{args.cipher}"\nError: {output["text"]}')

        mode = ""
        if args.decode:
            mode = "Decode"
        elif args.encode:
            mode = "Encode"
        elif args.brute:
            mode = "Brute"

        banner()

        if args.cipher == "pswd":
            print(
                f"""
        ------ Cipher: {args.cipher} -- Mode: {mode} ------
        Length   | {args.length}
        Password | {output['text']}
        ----
        """
            )
            return

        print(
            f"""
        ------ Cipher: {args.cipher} -- Mode: {mode} ------
        Input      | {args.text}
        Output     | {output['text']}

        Read File  | {args.input if args.input else "N/A"}
        Wrote File | {args.output if args.output else "N/A"}
        """
        )

        # remove output file from args for ciphers that manually write a file
        if args.cipher in ['qr', 'se', 'midify']:
            args.output = None

        # if output then output
        if args.output:
            with open(args.output, "w") as f:
                f.write(f"{output['text']}")


class Controller:

    def __init__(self, cipher_list):
        self.cipher_list = cipher_list
        self.cli = CLIManager(self.cipher_list)

    def run(self, user_args):
        from ..cryptex import check_argument
        output = None

        try:
            first_text = user_args[user_args.index("-t") + 1]
            user_args[user_args.index("-t") + 1] = f'"{first_text}"'
        except ValueError:
            first_text = "N/A"

        # if not self.check_argument(user_args, "cipher"):
        #     tr("No cipher selected.")
        #     return

        try:
            for arg in user_args:
                print(arg)
                if arg.lower() in self.cipher_list:
                    module = self.cipher_list[arg.lower()]
                else:
                    print(f'Cipher "{arg}" may not exist')
        except ValueError as e:
            print(e)

        func = None

        result = check_argument(user_args, "input")
        if result:
            index, value = result
            arg = user_args[index + 1]  # Get the value following the argument
            try:
                with open(arg, "r") as f:
                    data = f.readlines()
                    data = "".join(data)
                    # Why the hell is file content being added to the user_args list?
                    user_args[index + 1] = data  # Replace the value with the file content
            except UnicodeDecodeError:
                # can't read... probably because it's handled by cipher
                pass

        if check_argument(user_args, "encode"):
            func = module.encode
        elif check_argument(user_args, "decode"):
            func = module.decode
        elif check_argument(user_args, "brute"):
            func = module.brute
        else:
            print("No mode selected. see the help menu for more info")
            module.print_options()
            sys.exit()

        if output:
            arg = output["text"]

        output = func(arg)

        arg = first_text
        self.cli.print_output(output, arg)
