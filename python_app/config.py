import logging
from base64 import b64decode

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import googlemaps

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
    API_KEY = "API KEY"  # b64decode().decode() b64 encode Google API key

    @staticmethod
    def get_client():
        return googlemaps.client.Client(Config.API_KEY)
