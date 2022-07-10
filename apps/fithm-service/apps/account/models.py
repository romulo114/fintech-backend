from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Float,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import relationship

from libs.database import Base, Stateful, db_session
from apps.business.models import BusinessPrice

class Account(Stateful):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=True)
    business = relationship("Business", back_populates="accounts")
    portfolio = relationship("Portfolio", back_populates="accounts")
    account_positions = relationship(
        "AccountPosition",
        back_populates="account",
        cascade="all, delete, delete-orphan",
    )

    def as_dict(self):
        result = {
            "id": self.id,
            "account_number": self.account_number,
            "broker_name": self.broker_name,
            "portfolio_id": self.portfolio_id,
            "account_positions": [position.as_dict() for position in self.account_positions],
            "has_prices": self.has_prices,
            "has_cash_position": self.has_cash_position,
        }
        return result

    @property
    def has_prices(self):
        return True if all([account_position.has_price for account_position in self.account_positions]) else False

    @property
    def has_cash_position(self):
        return True if any([account_position.is_cash for account_position in self.account_positions]) else False


class AccountPosition(Stateful):
    __tablename__ = "account_positions"
    __table_args__ = (
        UniqueConstraint(
            "account_id", "symbol", name="account_positions_account_id_symbol_key"
        ),
    )
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    is_cash = Column(Boolean, nullable=True)
    account = relationship("Account", back_populates="account_positions")

    def as_dict(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "account_id": self.account_id,
            "broker_name": self.broker_name,
            "account_number": self.account_number,
            "symbol": self.symbol,
            "shares": str(self.shares),
        }


class AccountPositionPrice(Base):
    __tablename__ = "account_position_price"
    id = Column(Integer, primary_key=True)
    account_position_id = Column(
        Integer, ForeignKey("account_positions.id"), nullable=False
    )
    business_price_id = Column(Integer, ForeignKey("business_price.id"), nullable=False)

    @property
    def has_price(self):
        if db_session.query(BusinessPrice).get(self.business_price_id) > 0:
            return True
        return False
