from collections import defaultdict

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Boolean,
    Integer,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from apps.portfolio.models import Portfolio
from libs.database import Base, Stateful, db_session


class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    created = Column(DateTime, nullable=False)
    status = Column(
        "status",
        ENUM("active", "inactive", "retired", name="trade_status"),
        nullable=False,
    )
    business = relationship("Business", back_populates="trades")
    portfolios = relationship(
        "TradePortfolio", back_populates="trade", cascade="all, delete, delete-orphan"
    )

    @property
    def active_portfolios(self):
        portfolios = (
            db_session.query(Portfolio)
            .join(TradePortfolio, Portfolio.id == TradePortfolio.portfolio_id)
            .filter(
                TradePortfolio.active == True,
                TradePortfolio.trade_id == self.id,
            )
        )
        return portfolios

    @property
    def validated(self):
        return

    def as_dict(self, include_account_positions=False, include_model_positions=False):
        result = {
            "id": self.id,
            "name": self.name,
            "created": str(self.created),
            "status": str(self.status),
            "portfolios": [],
        }
        if self.portfolios:
            portfolios = [
                p.as_dict(
                    include_account_positions=include_account_positions,
                    include_model_positions=include_model_positions,
                )
                for p in self.portfolios
            ]
            portfolios.sort(key=lambda item: item['id'], reverse=True)
            result["portfolios"] = portfolios

            result["has_prices"] = (
                all([p.has_prices for p in self.active_portfolios]),
            )
            result["has_cash_positions"] = all(
                p.has_cash_positions for p in self.active_portfolios
            )

        return result

    def get_trade_positions(self):
        positions = []
        position_headers = ["trade_id", "portfolio_id", "account_number", "symbol", "shares"]
        for portfolio in self.active_portfolios:
            for account in portfolio.accounts:
                for account_position in account.account_positions:
                    positions.append(
                        [
                            self.id,
                            portfolio.id,
                            account.account_number,
                            account_position.symbol,
                            account_position.shares,
                        ]
                    )
        return position_headers, positions

    def get_model_positions(self):
        positions = []
        position_headers = ["trade_id", "portfolio_id", "model_id", "symbol", "weight"]
        for portfolio in self.active_portfolios:
            for model_position in portfolio.model.allocation:
                positions.append(
                    [
                        self.id,
                        portfolio.id,
                        model_position.model_id,
                        model_position.symbol,
                        model_position.weight,
                    ]
                )
        return position_headers, positions

    def get_unique_trade_positions(self):
        return set(self.get_trade_positions())

    def get_prices(self):
        price_headers = ["symbol", 'price']
        symbols_prices = []
        for portfolio in self.active_portfolios:
            for account in portfolio.accounts:
                symbols_prices.extend(account.get_prices())
            symbols_prices.extend(portfolio.model.get_prices())

        return price_headers, symbols_prices
        """

        :return: dict {symbol: price}
        """
        pass


class TradeRequest(Base):
    __tablename__ = "trade_requests"
    id = Column(Integer, primary_key=True)
    created = created = Column(DateTime, nullable=False)
    trade_id = Column(Integer, nullable=False)
    portfolio_id = Column(Integer, nullable=False)
    account_id = Column(Integer, nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    model_weight = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    restrictions = Column(String, nullable=False)


class TradePortfolio(Base):
    __tablename__ = "trade_portfolios"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "active", name="active_portfolio"),
    )
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer, ForeignKey("trades.id"))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    active = Column(Boolean, nullable=False)
    trade = relationship("Trade", back_populates="portfolios")
    portfolio = relationship("Portfolio", back_populates="trades")

    def as_dict(self, include_account_positions=False, include_model_positions=False):
        result = {
            "id": self.id,
            "trade_id": self.trade_id,
            "portfolio": self.portfolio.as_dict(
                include_account_positions=include_account_positions,
                include_model_positions=include_model_positions,
            ),
            "active": self.active,
        }
        return result
