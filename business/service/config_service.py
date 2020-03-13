import os
import json

CONFIG_PATH = 'config/'
CONFIG_FILE = 'config.json'


def __create_config_directory():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)


def set_last_retweet_id(last_retweet_id):
    if last_retweet_id:
        data = {
            'last_retweet_id': last_retweet_id
        }
        __create_config_directory()
        with open(CONFIG_PATH+CONFIG_FILE, "w+") as f:
            json.dump(data, f)


def get_last_retweet_id():
    try:
        with open(CONFIG_PATH+CONFIG_FILE, 'r') as f:
            config_dict = json.load(f)
            return config_dict['last_retweet_id']
    except OSError:
        return None
