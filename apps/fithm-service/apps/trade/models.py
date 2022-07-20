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
from libs.database import Base, Stateful
from libs.database.sql_base import db_session


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
        portfolios = db_session.query(TradePortfolio).filter(
            TradePortfolio.active == True,
            TradePortfolio.trade_id == self.id,
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
            result["portfolios"] = [
                p.as_dict(include_account_positions=include_account_positions,
                          include_model_positions=include_model_positions) for p in self.portfolios
            ]
            result["has_prices"] = all([p.has_prices for p in self.active_portfolios]),
            result["has_cash_positions"] = all(p.has_cash_positions for p in self.active_portfolios)

        return result

    def get_trade_positions(self):
        positions = []
        for portfolio in self.active_portfolios:
            positions.extend(portfolio.get_account_positions)
        return positions

    def get_unique_trade_positions(self):
        return set(self.get_trade_positions())

    def get_prices(self):
        d = defaultdict(set)
        for portfolio in self.portfolios:
            for account in portfolio.accounts:
                account_prices = account.get_prices()
                for key, value in account_prices.items:
                    d[key] = value
            model_prices = portfolio.model.get_prices()
            for key, value in model_prices:
                d[key] = value
        return d
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
            "portfolio": self.portfolio.as_dict(include_account_positions=include_account_positions,
                                                include_model_positions=include_model_positions),
            "active": self.active,
        }
        return result
