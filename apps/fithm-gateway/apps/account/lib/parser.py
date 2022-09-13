from flask_restx import reqparse
from flask import Request


class AccountParser:
    """Account endpoints arguments parser"""

    def __init__(self):
        self.create = None
        self.update = None
        self.position = None

    def parse_create(self, req: Request) -> dict:
        if not self.create:
            self.create = reqparse.RequestParser()
            self.create.add_argument(
                "broker_name", required=True, type=str, location="json"
            )
            self.create.add_argument(
                "account_number", required=True, type=str, location="json"
            )
            self.create.add_argument("portfolio_id", type=str, location="json")

        return self.create.parse_args(req)

    def parse_update(self, req: Request) -> dict:
        if not self.update:
            self.update = reqparse.RequestParser()
            self.update.add_argument("broker_name", type=str, location="json")
            self.update.add_argument("account_number", type=str, location="json")

        return self.update.parse_args(req)


    def parse_position_create(self, req: Request) -> dict:
        if not self.position:
            self.position = reqparse.RequestParser()
            self.update.add_argument("symbol", type=str, required=True, location="json")
            self.update.add_argument("shares", type=float, required=True, location="json")
            self.update.add_argument("is_cash", type=bool, required=True, location="json")

        return self.position.parse_args(req)
