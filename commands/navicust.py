import os
import json

# TODO Actually work this chip out.

command = "navicust"
use = "Navi customizer"

file_path = "/opt/Navi/config/custmizer.json"


def load_json(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data


def view_json(data, indent=2):
    print(json.dumps(data, indent=indent))


def edit_json(file_path, new_data):
    # Save the edited JSON to a temporary file
    temp_file = "_temp_" + os.path.basename(file_path)
    with open(temp_file, 'w') as f:
        json.dump(new_data, f, indent=2)

    # Replace the original JSON file with the edited version
    os.replace(temp_file, file_path)
