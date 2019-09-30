from base64 import b64encode
import logging

from flask import request

from utils.config import Config
from utils.response import MyResponse

_logger = logging.getLogger(__name__)


class DBOperations:

    @staticmethod
    def persist_to_db(table_name: 'Config.db.Model'):
        try:
            Config.db.session.add(table_name)
            Config.db.session.commit()
            _logger.info('%s was successfully added to db', table_name)
        except Exception as exc:
            _logger.exception('%s was not successfully added to db due to: %s', table_name, exc)
            Config.db.session.rollback()
            raise


class User(Config.db.Model):
    id = Config.db.Column(Config.db.Integer, primary_key=True)
    first_name = Config.db.Column(Config.db.String(), nullable=False)
    last_name = Config.db.Column(Config.db.String(), nullable=False)
    username = Config.db.Column(Config.db.String(), unique=True, nullable=False)
    email = Config.db.Column(Config.db.String(), unique=True, nullable=False)
    age = Config.db.Column(Config.db.Integer, nullable=False)
    password = Config.db.Column(Config.db.String(), nullable=True)
    google_map_data = Config.db.relationship('MapData', backref='user', lazy=True)

    def __init__(self, first_name: str, last_name: str, username: str,
                 email: str, age: int):
        self.first_name = first_name
        self.username = username
        self.last_name = last_name
        self.age = age
        self.email = email

    @classmethod
    def init_new(cls, user_data: request, username: str):
        return cls(
            first_name=user_data.json.get('first_name'),
            last_name=user_data.json.get('last_name'),
            username=username,
            email=user_data.json.get('email'),
            age=user_data.json.get('age'),
        )

    @staticmethod
    def get_id(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def set_password(username: str, password: str):
        encrypted_pass = b64encode(password.encode()).decode()
        try:
            set_user_pass = User.query.filter_by(username=username).first()
            set_user_pass.password = encrypted_pass
            Config.db.session.commit()
            _logger.info('Password set for %s user', username)
        except Exception as exc:
            _logger.exception('Password was not set for %s user due to: %s', username, exc)
            Config.db.session.rollback()
            raise

    @staticmethod
    def get_users():
        return MyResponse(
            message=[user.username for user in User.query.order_by(User.username).all()],
            status_code=Config.OK
        )

    @staticmethod
    def delete_from_user_db(username: str):
        try:
            User.query.filter_by(username=username).delete()
            Config.db.session.commit()
            _logger.info('%s user was successfully deleted', username.capitalize())
        except Exception as exc:
            _logger.exception('%s user was not deleted due to: %s', username.capitalize(), exc)
            Config.db.session.rollback()
            raise
