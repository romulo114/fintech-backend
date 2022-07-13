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
            TradePortfolio.active == True
        )
        return portfolios

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
        return result


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
        }
        return result
