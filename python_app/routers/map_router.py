import logging

from flask import request

from map import google_map
from utils.config import Config

_logger = logging.basicConfig(level=logging.INFO)


@Config.app.route("/api/v0/username/<username>/nearby_locations", methods=["GET"])
def get_nearby_data(username: str):
    return Config.create_response(
        response=google_map.get_nearby_data(username=username, location=request.json.get('location'))
    )


@Config.app.route("/api/v0/username/<username>/address", methods=["GET"])
def google_address(username: str):
    return Config.create_response(
        response=google_map.get_reverse_geocode_data(
            username=username, location=request.json.get('location'))
    )


if __name__ == "__main__":
    Config.db.create_all()
    Config.app.run(host="0.0.0.0")
