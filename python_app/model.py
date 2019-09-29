from base64 import b64encode
import json
import logging
from typing import Dict, Optional, Union, Any, Tuple, List

from flask import request
from flask_sqlalchemy import SQLAlchemy

from config import Config
from response import MyResponse

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
        user_record = User.query.filter_by(username=username).first()
        return user_record.id

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


class MapData(Config.db.Model):
    id = Config.db.Column(Config.db.Integer, primary_key=True)
    results = Config.db.Column(Config.db.String(), nullable=False)
    html_attributions = Config.db.Column(Config.db.String(), nullable=True)
    next_page_token = Config.db.Column(Config.db.String(), nullable=True)
    user_id = Config.db.Column(Config.db.Integer, Config.db.ForeignKey('user.id'), nullable=False)
    longitude = Config.db.Column(Config.db.Float, nullable=False)
    latitude = Config.db.Column(Config.db.Float, nullable=False)
    status = Config.db.Column(Config.db.String(), nullable=True)
    nearby_results = Config.db.Column(Config.db.String(), nullable=True)

    def __init__(self, user_id: int, coordinates: Tuple[float, float],
                 nearby_results: Optional[Dict[str, Any]] = None, status: Optional[str] = None,
                 token: Optional[str] = None, html_attr: Optional[str] = None,
                 results: Optional[str] = None):
        latitude, longitude = coordinates
        self.user_id = user_id
        self.next_page_token = token
        self.results = results
        self.html_attributions = html_attr
        self.longitude = longitude
        self.latitude = latitude
        self.status = status
        self.nearby_results = nearby_results

    @classmethod
    def init_new(cls, user_id: int, coordinates: Tuple[float, float],
                 nearby_results: Optional[Dict[str, Any]] = None, status: Optional[str] = None,
                 location_data: Optional[Dict[str, Union[str, int]]] = None,
                 token: Optional[str] = None, html_attr: Optional[str] = None,
                 results: Optional[str] = None):
        if location_data:
            token = location_data['next_page_token']
            results = str(location_data['results'])
            status = location_data['status']
            html_attr = location_data['html_attributions']
        return cls(
            user_id=user_id,
            status=status,
            token=token,
            results=results,
            html_attr=html_attr,
            coordinates=coordinates,
            nearby_results=json.dumps(nearby_results)
        )

    @staticmethod
    def user_history(username: str):
        user_id = User.get_id(username=username)
        return MyResponse(
            message=[result.results for result in MapData.query.filter_by(user_id=user_id).all()],
            status_code=Config.OK
        )

    @staticmethod
    def delete_from_map_db(username: str):
        try:
            MapData.query.filter_by(user_id=User.get_id(username=username)).delete()
            Config.db.session.commit()
            _logger.info('%s mapdata was successfully deleted', username.capitalize())
        except Exception as exc:
            _logger.exception('%s mapdata was not deleted due to: %s', username.capitalize(), exc)
            Config.db.session.rollback()
            raise
