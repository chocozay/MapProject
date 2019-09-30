import logging
import json
from typing import Tuple, Dict, Optional, Any, List, Union

import googlemaps

from utils.config import Config
from map import map_utils
from db.mapdata_model import MapData
from db.user_model import User, DBOperations
from utils.response import MyResponse

_logger = logging.getLogger(__name__)


def check_user(username: str) -> Union[MyResponse, int]:
    try:
        user = User.get_id(username=username)
        return user.id
    except AttributeError:
        return MyResponse(message=f"{username} does not exist", status_code=Config.NOT_FOUND)
    except Exception as exc:
        return MyResponse(message=f"Error occurred: {exc}", status_code=Config.INTERNAL_ERROR)


def get_places_nearby(location: Tuple[float, float]) -> Dict[str, Any]:
    return googlemaps.client.places_nearby(
        client=Config.get_client(),
        location=location,
        language='en',
        max_price=0,
        radius=1000,
    )


def get_an_address(location: Tuple[float, float]) -> List[str]:
    return googlemaps.client.reverse_geocode(
        client=Config.get_client(),
        latlng=location,
        language="en"
    )


# TODO Function needs work for better results
def get_nearby_data(username: str, location: Optional[Tuple[float, float]] = None) -> MyResponse:
    try:
        user_id = check_user(username=username)
        if isinstance(user_id, MyResponse):
            return user_id
        nearby_coordinates = map_utils.check_param_location(location)
        nearby_locations = get_places_nearby(location=nearby_coordinates)
        print(f"Nearby location: {nearby_locations}")
        new_map_data = MapData.init_new(
            user_id=user_id, coordinates=nearby_coordinates,
            location_data=map_utils.check_if_next_page_token_exist(nearby_locations)
        )
        DBOperations.persist_to_db(new_map_data)
        return MyResponse(
            message=f"Successfully got location data", status_code=Config.OK
        )
    except Exception as exc:
        return MyResponse(
            message=f"An error occurred: {exc}",
            status_code=Config.INTERNAL_ERROR
        )


def get_reverse_geocode_data(username: str, location: Optional[Tuple[float, float]]) -> MyResponse:
    try:
        user_id = check_user(username=username)
        if isinstance(user_id, MyResponse):
            return user_id
        coordinate_location = map_utils.check_param_location(location)
        address = get_an_address(location=coordinate_location)
        new_map_data = MapData.init_new(
            user_id=user_id, coordinates=coordinate_location,
            results=json.dumps(address)
        )
        DBOperations.persist_to_db(new_map_data)
        return MyResponse(
            message=f"Successfully got geocode data", status_code=Config.OK
        )
    except Exception as exc:
        return MyResponse(
            message=f"An error occurred: {exc}",
            status_code=Config.INTERNAL_ERROR
        )
