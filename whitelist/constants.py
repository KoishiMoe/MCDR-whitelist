import os
from pathlib import Path

PREFIX = '!!whitelist'
DATA_FOLDER = Path('config') / 'whitelist'
CONFIG_FILE = DATA_FOLDER / 'config.json'
LOG_FILE = DATA_FOLDER / 'logs.json'

os.makedirs(DATA_FOLDER, exist_ok=True)
