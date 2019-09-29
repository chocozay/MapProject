import logging

from flask import request
from sqlalchemy.exc import IntegrityError

from config import Config
from emailer import send_email
from model import User, DBOperations, MapData
from response import MyResponse

_logger = logging.getLogger(__name__)


def create_profile(user_data: request, username: str) -> MyResponse:
    try:
        new_user = User.init_new(user_data=user_data, username=username)
        DBOperations.persist_to_db(new_user)
        User.set_password(
            username=username,
            password=user_data.json.get("password")
        )
        content = f"Profile for {username} was created"
        email = user_data.json.get('email')
        send_email(content=content, subject="Profile Created", reciever=email)
        return MyResponse(
            content,
            Config.CREATED
        )

    except IntegrityError:
        return MyResponse(f"User {username} already exist", Config.CONFLICT)
    except Exception as exc:
        return MyResponse(f"Error occurred: {exc}", Config.INTERNAL_ERROR)


def delete_profile(username: str) -> MyResponse:
    try:
        MapData.delete_from_map_db(username=username)
        User.delete_from_user_db(username=username)
        return MyResponse(
            f"Profile for {username} was deleted",
            Config.DELETED
        )
    except Exception as exc:
        return MyResponse(f"Error occurred: {exc}", Config.INTERNAL_ERROR)


def get_user_history(username: str) -> MyResponse:
    try:
        return MapData.user_history(username=username)
    except Exception as exc:
        return MyResponse(f"Error occurred: {exc}", Config.INTERNAL_ERROR)


def get_all_users() -> MyResponse:
    try:
        return User.get_users()
    except Exception as exc:
        return MyResponse(f"Error occurred: {exc}", Config.INTERNAL_ERROR)
