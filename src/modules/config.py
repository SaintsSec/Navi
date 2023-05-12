# Imports.
import json
import os
import time

# Load the configuration from config.json.
with open('./var/pipes/config.json') as config_file:
    config = json.load(config_file)

# Prompt the user to enter new values for the configuration variables.
config['ai']['name'] = input("Enter AI's name: ")
config['ai']['gender'] = input("Enter gender option (male/female): ")
config['operator']['name'] = input("Enter your name: ")
print("(Setting nicknames can only be done by manually editing the config.json)\n")

# Save the updated configuration back to config.json.
with open('./var/pipes/config.json', 'w') as config_file:
    json.dump(config, config_file, indent=4)

# Print the updated configuration.
print("The configuration has been updated:")
print(json.dumps(config, indent=4))
time.sleep(5)

# Pause execution to allow the user to read the output
os.system("python3 ./navi.py"); exit()
