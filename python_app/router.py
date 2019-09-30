import logging

from flask import make_response, jsonify

from utils.config import Config
from utils.response import MyResponse
from routers.map_router import get_nearby_data, google_address
from routers.user_router import delete_user, create_user, get_all_users, history

_logger = logging.basicConfig(level=logging.INFO)


@Config.app.route("/", methods=["GET"])
def home():
    return create_response(MyResponse("Welcome!", 200))


def create_response(response: MyResponse):
    return make_response(jsonify(response.message), response.status_code)


if __name__ == "__main__":
    Config.db.create_all()
    Config.app.run(host="0.0.0.0")
