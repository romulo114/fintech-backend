from datetime import datetime
from typing import List, Optional
from libs.database.business import remove_free_business_prices
from flask import current_app, g, abort
from sqlalchemy import func
from libs.database import db_session
from .models import Account, AccountPosition, AccountPositionPrice
from apps.model.models import ModelPosition
from ..business.models import Business, BusinessPrice


class AccountView:
    def __init__(self):
        pass


    def get_accounts(self, params):
        """Get all accounts owned by business"""
        business: Business = g.business
        free = None
        if 'free' in params:
            free = params['free']

        current_app.logger.debug(free)
        accounts: List[Account] = business.accounts
        if free == 'portfolio':
            accounts = [acc for acc in accounts if acc.portfolio_id is None]
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
        for position in account.account_positions:
            if position.account_position_price:
                db_session.delete(position.account_position_price)
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


class AccountPositionsView:
    def __init__(self):
        pass


    def get_positions(self, account_id: int) -> list:
        """Get positions for the account"""

        account_positions = self.__get_account_positions(account_id)

        return [position.as_dict() for position in account_positions]


    def create_position(self, account_id: int, body: dict):
        """Create a new position for the account"""

        business_id = g.business.id
        account_position = AccountPosition(
            account_id=account_id,
            symbol=body['symbol'],
            shares=body['shares'],
            is_cash=body['is_cash']
        )

        business_price = self.__get_business_price(business_id, account_position.symbol)
        if business_price:
            account_position_price = AccountPositionPrice(
                account_position=account_position,
                account_price=business_price,
            )
            db_session.add(account_position_price)

        db_session.add(account_position)
        db_session.commit()

        return account_position.as_dict()


    def get_position(self, position_id: int) -> dict:

        position: AccountPosition = self.__get_account_position(position_id)
        if position is None:
            abort(404, "account position not found")

        return position.as_dict() if position else None


    def update_positions(self, id: int, body: dict) -> list:
        """Update positions for the account"""

        if 'positions' not in body:
            abort(400, "Bad request")
 
        current_app.logger.info(f'Update account positions: {body["positions"]}')
        business_id = g.business.id

        positions: list[dict] = body['positions']
        current_positions: list[AccountPosition] = self.__get_account_positions(id)
        business_prices = self.__get_business_prices(business_id)

        for pos in positions:
            new_price = pos["price"] if "price" in pos else None
            if "id" not in pos: # new position
                new_position = AccountPosition(
                    account_id=id,
                    symbol=pos["symbol"],
                    shares=pos["shares"],
                    is_cash=pos["is_cash"]
                )

                price = self.__find_or_create_price(
                    business_id,
                    business_prices,
                    new_position.symbol,
                    new_price
                )

                if price:
                    account_position_price = AccountPositionPrice(
                        account_position=new_position,
                        account_price=price,
                    )

                    db_session.add(account_position_price)

                db_session.add(new_position)
            else: # old position
                old_position = self.__find_account_position(current_positions, pos["id"])
                if "shares" in pos:
                    old_position.shares = pos["shares"]
                if "is_cash" in pos:
                    old_position.is_cash = pos["is_cash"]

                old_position_price: AccountPositionPrice = old_position.account_position_price
                old_position.symbol = pos["symbol"]
                price = self.__find_or_create_price(
                    business_id,
                    business_prices,
                    pos["symbol"],
                    new_price
                )

                if price:
                    if not old_position_price:
                        old_position_price = AccountPositionPrice(
                            account_position=old_position,
                            account_price=price,
                        )
                        db_session.add(old_position_price)

                    old_position_price.account_price = price
                else:
                    if old_position_price:
                        db_session.delete(old_position_price)

        # remove positions
        keep_position_ids = [pos["id"] for pos in positions if "id" in pos]
        for pos in current_positions:
            if pos.id in keep_position_ids:
                continue

            if pos.account_position_price:
                db_session.delete(pos.account_position_price)
            db_session.delete(pos)

        db_session.commit()

        # remove free business prices
        remove_free_business_prices(business_id)

        return [position.as_dict() for position in self.__get_account_positions(id)]


    def __get_account_positions(self, id: int) -> list[AccountPosition]:

        account: Account = db_session.query(Account).get(id)
        return account.account_positions


    def __get_business_prices(self, business_id: int) -> list[BusinessPrice]:
        return db_session.query(BusinessPrice).filter(
            BusinessPrice.business_id == business_id
        ).all()


    def __get_business_price(self, business_id: int, symbol: str) -> Optional[BusinessPrice]:

        return db_session.query(BusinessPrice).filter(
            BusinessPrice.business_id == business_id,
            BusinessPrice.symbol == symbol
        ).one_or_none()


    def __find_business_price(self, prices: list[BusinessPrice], symbol: str) -> Optional[BusinessPrice]:
        for price in prices:
            if price.symbol == symbol:
                return price

        return None


    def __get_account_position(self, position_id: int) -> AccountPosition:

        return db_session.query(AccountPosition).get(position_id)


    def __find_account_position(self, positions: list[AccountPosition], position_id: int) -> Optional[AccountPosition]:
        for position in positions:
            if position.id == position_id:
                return position

        return None


    def __find_or_create_price(
        self,
        business_id: int,
        prices: list[BusinessPrice],
        symbol: str,
        new_price: Optional[float]
    ) -> BusinessPrice:

        price = self.__find_business_price(prices, symbol)

        if not price:
            if not new_price:
                return None

            price = BusinessPrice(
                business_id=business_id,
                symbol=symbol,
                price=new_price
            )
            db_session.add(price)
        elif new_price:
            price.price = new_price

        return price
