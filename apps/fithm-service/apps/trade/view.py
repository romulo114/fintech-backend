from datetime import datetime
from flask import abort, current_app, g
from libs.database import db_session
from libs.database.trade import get_trade_prices, update_trade_prices, get_trade_instructions
from requests import HTTPError

from ..account.models import AccountPosition
from ..business.models import Business
from ..portfolio.models import Portfolio
from .models import Trade, TradePortfolio


class TradeView:
    def __init__(self):
        pass

    def get_trades(self) -> list:
        """Get all trades"""

        business: Business = g.business
        return {"trades": [trade.as_dict() for trade in business.trades]}

    def create_trade(self, param: dict) -> dict:
        """Create a new trade"""

        name = param["name"]
        trade = Trade(
            business_id=g.business.id,
            name=name,
            status="active",
            created=datetime.utcnow(),
        )
        db_session.add(trade)
        db_session.commit()

        return trade.as_dict()

    def get_trade(self, id: int) -> dict:
        """Get a trade details"""

        trade = self.__get_trade(id)
        return trade.as_dict()

    def update_trade(self, id: int, body: dict) -> dict:
        """Update a trade"""

        trade = self.__get_trade(id)
        status = body.get("status", trade.status)
        name = body.get("name", trade.name)
        trade.name = name
        trade.status = status
        db_session.commit()

        return trade.as_dict()

    def delete_trade(self, id: int):
        """Delete a trade"""

        trade = self.__get_trade(id)
        db_session.delete(trade)
        db_session.commit()

        return {"result": "success"}


    def get_instructions(self, id: int, send: bool = False ) -> list:
        """Get instructions"""
        trade = self.__get_trade(id)
        return get_trade_instructions(trade, send)


    def get_active_portfolios(self) -> list:
        portfolios = db_session.query(TradePortfolio).filter(
            TradePortfolio.active == True
        ).all()

        return [p.portfolio_id for p in portfolios]


    def update_portfolios(self, id: int, body: dict) -> list:
        """Get portfolios for the trade"""

        trade = self.__get_trade(id)
        if trade.status != "active":
            abort(400, "Not active model")

        portfolios = body["portfolios"]
        current_portfolios = [p.portfolio_id for p in trade.portfolios or []]
        new_portfolios = [id for id in portfolios if id not in current_portfolios]

        portfolios_to_remove = [id for id in current_portfolios if id not in portfolios]

        # Todo update to not delete tradeportfolio and instead mark as "inactive"
        db_session.query(TradePortfolio).filter(
            TradePortfolio.portfolio_id.in_(portfolios_to_remove),
            TradePortfolio.trade_id == id
        ).delete(False)

        new_items = [
            TradePortfolio(trade_id=id, portfolio_id=port_id, active=True)
            for port_id in new_portfolios
        ]
        db_session.add_all(new_items)

        db_session.commit()
        return self.__get_trade(id).as_dict()


    def update_portfolio(self, trade_id: int, portfolio_id: int, body: dict) -> None:
        active = body['active']
        trade_portfolio: TradePortfolio = db_session.query(TradePortfolio).filter(
            TradePortfolio.portfolio_id == portfolio_id,
            TradePortfolio.trade_id == trade_id
        ).one_or_none()

        if not trade_portfolio:
            abort(404, 'Trade portfolio not found')

        trade_portfolio.active = active
        db_session.commit()


    def get_positions(self, id: int, args: dict) -> list:
        """Get positions for the trade"""

        trade = self.__get_trade(id)
        if "portfolio_id" in args and args["portfolio_id"]:
            portfolio = db_session.query(Portfolio).get(args["portfolio_id"])
            positions = portfolio.account_positions
        else:
            trade_portfolios: list[TradePortfolio] = trade.portfolios
            portfolios: list[Portfolio] = [p.portfolio_id for p in trade_portfolios]
            positions = (
                db_session.query(AccountPosition)
                .filter(AccountPosition.portfolio_id.in_(portfolios))
                .all()
            )

        return [position.as_dict() for position in positions]


    def update_positions(self, id: int, body: dict) -> dict:
        """Update positions for the trade"""

        # positions = body['positions']
        # trade = self.__get_trade(id)
        # positions: list[AccountPosition] = get_account_positions(positions)
        # update_account_positions(trade, positions)

        return self.__get_trade(id).as_dict()


    def get_prices(self, id: int) -> list:
        """Get prices for the trade"""

        trade = self.__get_trade(id)
        prices = get_trade_prices(trade)
        if prices is None:
            return []
        else:
            return [p.as_dict() for p in prices["price_object"]]


    def update_prices(self, id: int, body: dict) -> dict:
        """Update prices for the trade"""

        if "iex" not in body or not body["iex"]:
            prices = None
        else:
            prices = body["prices"]

        trade = self.__get_trade(id)
        result = update_trade_prices(trade, prices)

        if isinstance(result, str):
            return {"error": result}, 400
        else:
            return self.__get_trade(id).as_dict()


    def get_requests(self, id: int) -> list:
        """Get all requests for the trade"""

        trade = self.__get_trade(id)
        return {"requests": get_trade_instructions(trade)}


    def __get_trade(self, id: int) -> Trade:

        return db_session.query(Trade).get(id)
