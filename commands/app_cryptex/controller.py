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

        for key in self.cipher_types:
            print("|" + self.__add_extra(f"-- {key}s", len(self.line), "-") + "|-- short name ------|")
            for item in self.cipher_types[key]:
                print("|      " + self.__add_extra(item[0], 30, " ") + f" |      {item[1]} \t   |")
        print("|" + self.line + "|" + self.__add_extra("", 20, "-") + "|")


class Controller:

    def __init__(self, cipher_list):
        self.cipher_list = cipher_list
        self.cli = CLIManager(self.cipher_list)

    def run(self, user_args):
        from ..cryptex import check_argument, get_argument_value
        output = None

        try:
            first_text = user_args[user_args.index("-t") + 1]
            user_args[user_args.index("-t") + 1] = f'"{first_text}"'
        except ValueError:
            first_text = "N/A"

        module = None
        selected_cipher = None
        try:
            for arg in user_args:
                if arg.lower() in self.cipher_list:
                    module = self.cipher_list[arg.lower()]
                    selected_cipher = arg.lower()
        except ValueError as e:
            print(e)
        if module is None:
            tr("No cipher selected. see the help menu for more info")

        if check_argument(user_args, "test"):
            print('\n')
            status = [0, 0]
            for k, v in self.cipher_list.items():
                try:
                    out = v.test(user_args)
                except Exception as e:
                    print(f"{Fore.YELLOW}No test for {k}{Fore.WHITE}\n\t{e}")
                else:
                    color = Fore.GREEN
                    msg = "Success:"

                    if out['status']:
                        status[0] += 1
                    else:
                        status[1] += 1
                        color = Fore.RED
                        msg = "Failed: "
                    print(f"{color}{msg} {k} {'-' * (15 - len(k))} {out['msg']}{Fore.WHITE}")

            total = status[0] + status[1]
            print(f"{Fore.GREEN}Success{Fore.WHITE}/{Fore.RED}Failed {Fore.WHITE}{status[0]}/{status[1]}")

            if total != 0:
                percent = (status[0] / total) * 100
                print(f"Success percentage {percent}%")
            else:
                print("Total is zero, cannot compute success percentage.")
            return

        func = None

        result = check_argument(user_args, "input")
        if result:
            index, value = result
            arg = user_args[index + 1]  # Get the value following the argument
            try:
                with open(arg, "r") as f:
                    data = f.readlines()
                    data = "".join(data)
                    text_result = check_argument(user_args, "text")
                    if text_result:
                        user_args[text_result[0] + 1] = data  # Replace the value with the file content
                    else:
                        user_args.insert(index + 1, "-t")
                        user_args.insert(user_args.index("-t") + 1, data)  # Replace the value with the file content
            except UnicodeDecodeError:
                # can't read... probably because it's handled by cipher
                pass

        if check_argument(user_args, "encode"):
            func = module.encode(user_args)
        elif check_argument(user_args, "decode"):
            func = module.decode(user_args)
        elif check_argument(user_args, "brute"):
            func = module.brute(user_args)
        else:
            tr("No mode selected. see the help menu for more info")
            module.print_options(self)
            return
        if func['success']:
            print(selected_cipher)
            if check_argument(user_args, "output") and selected_cipher not in ['qr', 'se', 'midify']:
                try:
                    output_location = get_argument_value(user_args, "output")
                    with open(output_location, "w") as f:
                        f.write(func['text'])
                        # Open the file in the default text editor
                        import subprocess
                        import platform
                        import os
                        tr(f"Done! Attempting to open {output_location} in default text editor")
                        if platform.system() == 'Linux':
                            # For Unix-like operating systems
                            subprocess.call(["xdg-open", output_location])
                        elif platform.system() == 'Windows':
                            # For Windows
                            os.startfile(output_location)
                        elif platform.system() == 'Darwin':
                            # For macOS
                            subprocess.call(["open", output_location])
                        return
                except Exception as e:
                    tr(f"Error writing to file: {e}")
                    return
        tr(f"Done!\n{func['text']}" if func['success'] else f"Ah! Something went wrong: {func['text']}")
