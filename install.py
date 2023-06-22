#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports.
import sys # System stuff.
import os # Operating System functions.

# Distro package manager commands
class Distros:
    @staticmethod
    def debian():
        return [
            'sudo apt update',
            'sudo apt-get install -y python3 python3-pip python-dev nmap macchanger clamav',
        ]
    @staticmethod
    def arch():
        return [
            'sudo pacman -Syu',
            'sudo pacman -S python python-pip nmap machanger-git clamav',
        ]
    @staticmethod
    def void():
        return Distros.debian()
    @staticmethod
    def opensuse():
        return [
            'sudo zypper in python310 nmap macchanger clamav',
        ]
        # Do I need to add more here?

def handle_distros():
    # Distros
    distros = {
        'Debian': [
            'Parrot',
            'Ubuntu',
            'Kali',
            'Mint',
        ],
        'Arch': [
            'Garuda',
            'Manjaro',
        ],
        'Void' : [],
        'openSUSE': [
            'openSUSE Tumbleweed',
            'openSUSE Leap',
        ]
    }

    # auto detect
    distro = os.popen('cat /etc/issue').read()
    auto = '- Unsupported disto'
    for k, v in distros.items():
        if k.lower() in distro.lower():
            auto = f'- {k}'
            break
        else:
            txt = ''
            for sub in v:
                if sub.lower() in distro.lower():
                    txt = f'- {k} ({sub})'
                    break
            if txt != '':
                auto = txt
                break

    message = ''
    for key, val in distros.items():
        message += f'\n\t- {key}'
        for sub in val:
            message += f'\n\t    - {sub}'
    
    print(f"""
        - auto
            {auto}{message}
        """)

    ans = ''
    while not ans in [k.lower() for k, _ in distros.items()] + ['auto']: 
        # user input to select a distro
        ans=input("Navi> What is your operating system?: ").lower()

    if 'auto' in ans:
        ans = auto.split('- ')[1].lower()

    if 'debian' in ans:
        return Distros.debian()
    elif 'arch' in ans:
        return Distros.arch()
    elif 'void' in ans:
        return Distros.void()
    elif 'opensuse' in ans:
        return Distros.opensuse()
    
    print(f'\n\tNavi> [!!] - Unsuported distro: {ans}\n')
    exit(1)

def check_shell_config(location):
    # check if the navi alias is in the given file
    with open(location, 'rt') as f:
        check = 'alias navi-e1' in f.read()
    return check
    
def handle_shell():
    shell = os.readlink(f'/proc/{os.getppid()}/exe')

    # Display a unsuported shell message if the shell isn't suported
    message = '\n\t\tNavi> [!!] - Unsuported shell'
    supported = ['bash', 'zsh', 'fish']
    for s in supported:
        if s in shell:
            message = ''
            break

    # Auto generate the list of shels
    shells = ''
    for s in supported:
        shells += f'\n\t- {s}'
    print(f"""
        - auto
            - {shell}{message}{shells}
    """)

    # Check for input
    ans = ''
    options = ['auto'] + supported
    while ans not in options:
        ans=input("Navi> [!!] - What is your shell?: ").lower()

    # If the input was not 'auto' then set the shell to what the user entered
    if 'auto' not in ans:
        shell = ans

    # set the path to the config based on what shell you are setting it up for
    user = os.environ['HOME']
    path = ''
    if 'bash' in shell:
        path = f'{user}/.bashrc'
    elif 'zsh' in shell:
        path = f'{user}/.zshrc'
    elif 'fish' in shell:
        path = f'{user}/.config/fish/config.fish'
    else:
        print(f'\n\tNavi> [!!] - Unsuported shell: {shell}\n')
        exit(1)

    # Check if the cyrptex alias already exists in the given shell
    if check_shell_config(path):
        print(f'\n\tNavi> [!!] - Alias already exists in config: {path}\n')
        return ''

    command = 'echo \'alias navi="cd ~/.Navi && python3 navi.py && cd"\'' 
    return f'{command} >> {path}'
    
def main():
    # Check for updates
    #from src import Update
    #Update()

    # List over commands to run
    commands = []

    commands += handle_distros()

    # Cryptex related commands
    commands += [
        'sudo freshclam',
        'rm -rf ~/.Navi',
        'mkdir ~/.Navi',
        'cp -r . ~/.Navi',
        'rm -rf ~/.Navi/.git/',
        'rm -rf ~/.Navi/.github/',
        'rm -rf ~/.Navi/demo/',
        'rm ~/.Navi/README.md',
        'rm ~/.Navi/CONTRIBUTING.md',
        'rm ~/.Navi/CODE_OF_CONDUCT.md',
        'rm ~/.Navi/install.py',
        'rm -rf ~/.Navi/RAD',
    ]

    # Shell related commands
    commands += [handle_shell()]

    # Run the commands
    for c in commands:
        if len(c) <= 0: continue
        print(f'\n\tNavi> [!!] - RUNNING: {c}\n')
        os.system(c)

    # End message
    print("""
    Navi> [!!] - Installation finished.
    Navi> [!!] - Restart the terminal and MAKE SURE YOU RUN neuralset.py before launching.
    """)
    exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nYou interrupted the program.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
