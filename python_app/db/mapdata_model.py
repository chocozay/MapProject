import json
import logging
from typing import Dict, Optional, Union, Any, Tuple

from db.user_model import User
from utils.config import Config
from utils.response import MyResponse

_logger = logging.getLogger(__name__)


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
        user = User.get_id(username=username)
        if user is not None:
            user_id = user.id
            return MyResponse(
                message=[result.results for result in MapData.query.filter_by(user_id=user_id).all()],
                status_code=Config.OK
            )
        else:
            return MyResponse(
                message=f"User '{username}' does not exist",
                status_code=Config.NOT_FOUND
            )

    @staticmethod
    def delete_from_map_db(username: str):
        try:
            MapData.query.filter_by(user_id=User.get_id(username=username).id).delete()
            Config.db.session.commit()
            _logger.info('%s mapdata was successfully deleted', username.capitalize())
        except Exception as exc:
            _logger.exception('%s mapdata was not deleted due to: %s', username.capitalize(), exc)
            Config.db.session.rollback()
            raise
