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

    def as_dict(self, include_account_positions=True):
        result = {
            "id": self.id,
            "account_number": self.account_number,
            "broker_name": self.broker_name,
            "portfolio_id": self.portfolio_id,
            "has_prices": self.has_prices,
            "has_cash_position": self.has_cash_position,
        }
        if include_account_positions:
            result["account_positions"] = (
                [position.as_dict() for position in self.account_positions],
            )
        return result

    @property
    def has_prices(self):
        return (
            True
            if all(
                [
                    account_position.account_position_price.has_price
                    for account_position in self.account_positions
                ]
            )
            else False
        )

    @property
    def has_cash_position(self):
        return (
            True
            if any(
                [
                    account_position.is_cash
                    for account_position in self.account_positions
                ]
            )
            else False
        )


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
    account_position_price = relationship(
        "AccountPositionPrice", back_populates="account_position", uselist=False
    )

    def as_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "symbol": self.symbol,
            "shares": str(self.shares),
            "price": self.account_position_price.price.as_dict(),
        }


class AccountPositionPrice(Base):
    __tablename__ = "account_position_price"
    id = Column(Integer, primary_key=True)
    account_position_id = Column(
        Integer,
        ForeignKey("account_positions.id"),
        nullable=False,
    )
    business_price_id = Column(Integer, ForeignKey("business_price.id"), nullable=False)
    is_manual = Column(Boolean)
    account_position = relationship(
        "AccountPosition", back_populates="account_position_price"
    )
    account_price = relationship("BusinessPrice", back_populates="account_position_prices")

    @property
    def has_price(self):
        if (
            db_session.query(BusinessPrice.price)
            .filter(BusinessPrice.id == self.business_price_id)
            .one()[0]
            > 0
        ):
            return True
        return False
