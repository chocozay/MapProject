import logging

_logger = logging.getLogger(__name__)


class MyResponse:

    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"[{self.status_code}] {self.message}"
