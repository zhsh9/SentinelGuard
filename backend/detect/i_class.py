"""
Define the class for the IDS.
"""
import json

CONFIG_FILE_PATH = '../../i_class.json'

def load_config(file_path: CONFIG_FILE_PATH): # type: ignore
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    config = load_config(CONFIG_FILE_PATH)
    print(config)