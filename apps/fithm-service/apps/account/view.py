from typing import List
from flask import current_app, g, abort
from libs.database import db_session
from .models import Account, AccountPosition
from ..business.models import Business


class AccountView:
    def __init__(self):
        pass

    def get_accounts(self):
        """Get all accounts owned by business"""
        business: Business = g.business
        accounts: List[Account] = business.accounts
        return {
            "accounts": [account.as_dict() for account in accounts if account.active]
        }

    def create_account(self, body: dict) -> dict:
        """Create a new account for the business"""

        # check existence
        accounts = (
            db_session.query(Account)
            .filter(
                Account.broker_name == body["broker_name"],
                Account.account_number == body["account_number"],
            )
            .all()
        )
        if len(accounts):
            abort(403, "Account already exists")

        # create an account
        account = Account(
            business_id=g.business.id,
            broker_name=body["broker_name"],
            account_number=body["account_number"],
        )
        if "portfolio_id" in body and body["portfolio_id"]:
            account.portfolio_id = body["portfolio_id"]

        db_session.add(account)
        db_session.commit()

        return account.as_dict()

    def get_account(self, id: int):
        """Get account detail"""

        account = self.__get_account(id)
        if not account.active:
            abort(401, "Not active account")

        return account.as_dict()

    def update_account(self, id: int, body: dict) -> dict:
        """Update an existing account"""

        account = self.__get_account(id)
        if "account_number" in body:
            account.account_number = body["account_number"]
        if "broker_name" in body:
            account.broker_name = body["broker_name"]

        db_session.commit()
        return account.as_dict()

    def delete_account(self, id: int):
        """
        Delete an account"""

        account = self.__get_account(id)
        db_session.delete(account)
        db_session.commit()

        return {"result": "success"}

    def __get_account(self, id: int) -> Account:

        account = db_session.query(Account).get(id)
        if not account:
            abort(404, "Account not found")
        if account.business_id != g.business.id:
            abort(403, "You don't have permission to this account.")

        return account


class AccountPositionView:
    def __init__(self):
        pass

    def get_positions(self, id: int, args: dict) -> list:
        """Get positions for the account"""

        account = self.__get_account(id)

        return [position.as_dict() for position in account.positions]

    def update_positions(self, id: int, body: dict) -> dict:
        """Update positions for the account"""

        positions = body['positions']
        current_positions: list[AccountPosition] = self.__get_account_positions(id)
        new_positions = [position for position in positions if "id" not in position.keys()]
        remove_positions = filter(lambda id: id not in positions, current_positions)

        # Todo update to not delete tradeportfolio and instead mark as "inactive"

        for position in remove_positions:
            position.active = False
            db_session.add(position)
        new_items = [
            AccountPosition(account_id=id, symbol=position["symbol"], shares=position["shares"], active=True)
            for position in new_positions
        ]
        db_session.add_all(new_items)
        db_session.commit()

        return self.__get_account_positions(id).as_dict()

    def __get_account_positions(self, id: int) -> AccountPosition:

        return db_session.query(Account).get(id).account_positions