import datetime
from typing import List
from flask import current_app, g, abort
from libs.database import db_session
from .models import Account, AccountPosition, AccountPositionPrice
from ..business.models import Business, BusinessPrice


class AccountView:
    def __init__(self):
        pass


    def get_accounts(self):
        """Get all accounts owned by business"""
        business: Business = g.business
        accounts: List[Account] = business.accounts
        current_app.logger.debug(accounts)
        return {
            "accounts": [account.as_dict(False) for account in accounts if account.active]
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


    def get_positions(self, id: int, args: dict = None) -> list:
        """Get positions for the account"""

        account_positions = self.__get_account_positions(id)

        return [position.as_dict() for position in account_positions]


    def create_position(self, id: int, body: dict):
        position = AccountPosition(
            account_id=id,
            symbol=body['symbol'],
            shares=body['shares'],
            is_cash=body['is_cash'],
            price=[] if 'prices' in body else body['prices']
        )

        db_session.add(position)
        db_session.commit()

        return position.as_dict()


    def update_positions(self, id: int, body: dict) -> list:
        """Update positions for the account"""
        business_id = body["business_id"]
        positions = body["positions"]
        current_positions: list[AccountPosition] = self.__get_account_positions(id)
        new_positions = [
            position for position in positions if "id" not in position.keys()
        ]
        remove_positions = filter(lambda id: id not in positions, current_positions)
        keep_positions = filter(lambda id: id in positions, current_positions)
        # todo update current positions shares if changed.

        for position in remove_positions:
            position.active = False
            db_session.add(position)
        new_items = [
            AccountPosition(
                account_id=id,
                symbol=position["symbol"],
                shares=position["shares"],
                active=True,
            )
            for position in new_positions
        ]
        for account_position in new_items:
            business_price = (
                db_session.query(BusinessPrice)
                .filter(
                    BusinessPrice.id == business_id,
                    BusinessPrice.symbol == account_position.symbol,
                )
                .one_or_none()
            )
            if business_price:
                db_session.add(
                    AccountPositionPrice(
                        account_position=account_position,
                        price=business_price,
                    )
                )
            else:
                new_business_price = BusinessPrice(
                    business_id=business_id,
                    symbol=account_position.symbol,
                    updated=datetime.datetime.now(),
                )
                db_session.add(new_business_price)
                db_session.flush()
                db_session.add(
                    AccountPositionPrice(
                        account_position=account_position,
                        business_price_id=new_business_price.id,
                    )
                )
        db_session.add_all(new_items)

        db_session.commit()

        return [position.as_dict() for position in self.__get_account_positions(id)]


    def __get_account_positions(self, id: int) -> list[AccountPosition]:

        account: Account = db_session.query(Account).get(id)
        return account.account_positions
