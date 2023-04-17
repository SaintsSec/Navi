#! /bin/python3

import os

def installNavi():
    print("Totally Janky Navi Mac Installer")
    os.system('pip install -r requirements.txt')
    os.system('sudo rm -rf ~/.Navi/')
    os.system('mkdir ~/.Navi/')
    os.system('cp -r . ~/.Navi/')

def naviAlias():
    path = "~/.zshrc"
    command = 'echo \'alias navi = "python3 ~/.Navi/src/main.py"\''
    return f'{command} >> {path}'

installNavi()
naviAlias()
