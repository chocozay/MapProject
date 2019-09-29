import getpass
from json import loads, load

import logging
import requests
from typing import Optional, Dict, Any

domain = "http://0.0.0.0:5000/api/v0/username"
logging.getLogger(__name__)


def read_config_file(file_path):
    with open(file_path, 'r') as config_file:
        user_data = load(config_file)
    if 'password' in user_data.keys():
        raise IndexError('Password field should not be included')
    user_data.update({'password': getpass.getpass('Password: ')})
    return user_data


def get_all_user():
    return requests.get(url=domain).json()


def setup_user(username: str) -> Dict[str, Any]:
    user_payload = {}
    user_payload.update({"first_name": input("Enter first name: ")})
    user_payload.update({"last_name": input("Enter last name: ")})
    user_payload.update({"username": username})
    user_payload.update({"email": input("Enter email: ")})
    user_payload.update({"age": input("Enter age: ")})
    user_payload.update({"password": getpass.getpass('Password: ')})
    return user_payload


def create_user(username: str, config_file: Optional[str] = None):
    payload = read_config_file(config_file) if config_file else setup_user(username=username)
    return requests.post(url=f"{domain}/{username}", json=payload).json()


def delete_user(username: str):
    return requests.delete(url=f"{domain}/{username}").json()


def get_user_history(username: str):
    history = requests.get(url=f"{domain}/{username}/history").json()
    if not history:
        logging.error("No search history was found")
    for index, results in enumerate([loads(result) for result in history if loads(result)], 1):
        if isinstance(results, list):
            for result_index, result in enumerate(results, 1):
                logging.info("[#%s] Sub results entry: %s\n", result_index, result)
        else:
            logging.info("[#%s] Results DB entry: %s\n", index, results)
    return history


# TODO be implemented
def get_nearby_location(username: str):
    url = f"{domain}/{username}/nearby_locations"
    pass


# TODO be implemented
def get_address(username: str):
    url = f"{domain}/{username}/address"
    pass
