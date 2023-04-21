import os

command = "/macchanger"
use = "Change your mac adress"

def run():
    print('''
What would you like to do? 
  1. Random Mac 
  2. Custom Mac''')
    mode = input('Mode => ')
	
    if mode in ['1', '2']:
	print('Please select an interface, for example "eth0"')
	interface = input('Interface => ')
	if mode == '1':
	    random(interface)
	elif mode == '2':
	    custom(interface)
    else:
	print(f'Invalid input "{mode}"')

def cmd(cmds):
    cmd = ' && '.join(cmds)
    os.system(cmd)

def random(interface):
    print('Using random MAC addesss')
    cmd([
        'ifconfig down',
        f'macchanger -r {interface}',
        'ifconfig up'
    ])

def custom(interface):
    mac = input('Mac Adress => ')
    print(f'Using specified mac address "{mac}"')
    cmd([
        'ifconfig down',
        f'macchanger --mac="{mac}" {interface}',
        'ifconfig up'
    ])

