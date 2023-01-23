from flask_restx import reqparse
from flask import Request


class BusinessParser:
    """Account endpoints arguments parser"""

    def __init__(self):
        self.create = None

    def parse_price_create(self, req: Request) -> dict:
        if not self.create:
            self.create = reqparse.RequestParser()
            self.create.add_argument("symbol", required=True, type=str, location="json")
            self.create.add_argument("price", required=True, type=float, location="json")

        return self.create.parse_args(req)
