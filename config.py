'''Reads and store game config as global variable.

Config have to be placed in root directory and named `config.json`, example
config file should be provided in main directory.

If content of file testing in root directory is set to '1' then testing config
is loaded.
'''
import json
import os
import logging

logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

config = {}
test = '0'
with open('testing', 'r') as file_handler:
    test = file_handler.readline()

path = 'tests/test_config.json' if test == '1' else 'config.json'
with open(path, 'r') as file_handler:
            config = json.load(file_handler)

logger.warning("Config loaded from file {}".format(path))
