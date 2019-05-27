'''Reads and store game config as global variable.

Config have to be placed in root directory and named `config.json`, example
config file should be provided in main directory.
'''
import json

config = {}
with open('config.json', 'r') as file_handler:
            config = json.load(file_handler)