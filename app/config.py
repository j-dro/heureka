import os
from shared.configuration import Configuration

CONFIG_PATH = os.path.join(os.path.dirname(__file__))
CONFIG_FILE = 'config.yaml'
CONFIG_FILE_LOCAL = 'config.local.yaml'

try:
    configuration = Configuration.from_file(os.path.join(CONFIG_PATH, CONFIG_FILE_LOCAL))
except FileNotFoundError:
    configuration = Configuration.from_file(os.path.join(CONFIG_PATH, CONFIG_FILE))
