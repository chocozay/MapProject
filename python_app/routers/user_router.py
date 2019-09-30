import logging

from flask import request

from users import user
from utils.config import Config

_logger = logging.basicConfig(level=logging.INFO)


@Config.app.route("/api/v0/username", methods=["GET"])
def get_all_users():
    return Config.create_response(response=user.get_all_users())


@Config.app.route("/api/v0/username/<username>", methods=["POST"])
def create_user(username: str):
    return Config.create_response(
        response=user.create_profile(username=username, user_data=request)
    )


@Config.app.route("/api/v0/username/<username>", methods=["DELETE"])
def delete_user(username: str):
    return Config.create_response(response=user.delete_profile(username=username))


@Config.app.route("/api/v0/username/<username>/history", methods=["GET"])
def history(username: str):
    return Config.create_response(user.get_user_history(username=username))


if __name__ == "__main__":
    Config.db.create_all()
    Config.app.run(host="0.0.0.0")
