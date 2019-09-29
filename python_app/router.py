import logging

from flask import make_response, request, jsonify

import google_map
from python_app import user
from config import Config
from response import MyResponse

_logger = logging.basicConfig(level=logging.INFO)


@Config.app.route("/", methods=["GET"])
def home():
    return create_response(MyResponse("Welcome!", 200))


@Config.app.route("/api/v0/username", methods=["GET"])
def get_all_users():
    return create_response(response=user.get_all_users())


@Config.app.route("/api/v0/username/<username>", methods=["POST"])
def create_user(username: str):
    return create_response(response=user.create_profile(username=username, user_data=request))


@Config.app.route("/api/v0/username/<username>", methods=["DELETE"])
def delete_user(username: str):
    return create_response(response=user.delete_profile(username=username))


@Config.app.route("/api/v0/username/<username>/nearby_locations", methods=["GET"])
def get_random_info(username: str):
    return create_response(
        response=google_map.get_nearby_data(username=username, location=request.json.get('location'))
    )


@Config.app.route("/api/v0/username/<username>/address", methods=["GET"])
def google_address(username: str):
    return create_response(
        response=google_map.get_reverse_geocode_data(
            username=username, location=request.json.get('location'))
    )


@Config.app.route("/api/v0/username/<username>/history", methods=["GET"])
def history(username: str):
    return create_response(user.get_user_history(username=username))


def create_response(response: MyResponse):
    return make_response(jsonify(response.message), response.status_code)


if __name__ == "__main__":
    Config.db.create_all()
    Config.app.run(host="0.0.0.0")
