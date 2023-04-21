import os

command = "/macchanger"
use = "Change your mac adress"

def run():
    print('''
Navi> What would you like to do? 
  1. Random Mac 
  2. Custom Mac''')
    mode = input('Navi> Which mode(Ex: 1 / 2) => ')
	
    if mode in ['1', '2']:
        print('Navi> Please select an interface, for example "eth0"')
        interface = input('Navi> Which interface => ')
        if mode == '1':
            random(interface)
        elif mode == '2':
            custom(interface)
    else:
        print(f'Navi> [!!] - Invalid input "{mode}"')

def cmd(cmds):
    cmd = ' && '.join(cmds)
    os.system(cmd)

def random(interface):
    print('Navi> [\u2713] - Using random MAC addesss')
    cmd([
        'ifconfig down',
        f'macchanger -r {interface}',
        'ifconfig up'
    ])

def custom(interface):
    mac = input('Mac Adress => ')
    print(f'Navi> [\u2713] - Using specified mac address "{mac}"')
    cmd([
        'ifconfig down',
        f'macchanger --mac="{mac}" {interface}',
        'ifconfig up'
    ])

