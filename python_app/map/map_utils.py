from random import random, randint
from typing import Tuple, Dict, Optional, List

from utils.config import Config


def get_random_latitude() -> float:
    return round(
        randint(Config.MIN_LATITUDE, Config.MAX_LATITUDE) + random(), Config.TRUNC_VALUE
    )


def get_random_longitude() -> float:
    return round(
        randint(Config.MIN_LONGITUDE, Config.MAX_LONGITUDE) + random(), Config.TRUNC_VALUE
    )


def check_param_location(location: List[float]):
    if location and isinstance(location, list):
        print("Location returned")
        return location
    print("Random location generated")
    return get_random_location()


def get_random_location() -> Tuple[float, float]:
    return get_random_latitude(), get_random_longitude()


def check_if_next_page_token_exist(location_data: Dict[str, Optional[str]]):
    if "next_page_token" not in location_data.keys():
        location_data.update({'next_page_token': None})
    return location_data
