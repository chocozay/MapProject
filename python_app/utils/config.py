import logging
from base64 import b64decode
from os import getenv

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import googlemaps

from utils.response import MyResponse

_logger = logging.getLogger(__name__)


class Config:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/myproject"
    db = SQLAlchemy(app)
    TRUNC_VALUE = 7
    MAX_LATITUDE = 89
    MIN_LATITUDE = -90
    MAX_LONGITUDE = 179
    MIN_LONGITUDE = -180
    DELETED = 202
    CREATED = 201
    OK = 200
    INTERNAL_ERROR = 500
    NOT_FOUND = 404
    CONFLICT = 409
    API_KEY = b64decode(getenv("API_KEY").encode()).decode()

    @staticmethod
    def get_client():
        return googlemaps.client.Client(Config.API_KEY)

    @staticmethod
    def create_response(response: MyResponse):
        return make_response(jsonify(response.message), response.status_code)
