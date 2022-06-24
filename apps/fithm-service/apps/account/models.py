from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Float, UniqueConstraint
)
from sqlalchemy.orm import relationship
from libs.database import Base, Stateful


class Account(Stateful):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('business.id'), nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=True)
    cash_position_price_id = Column(Integer, ForeignKey('account_position_price.id'), nullable=True, name="cash_position_price")
    business = relationship("Business", back_populates="accounts")
    portfolio = relationship("Portfolio", back_populates="accounts")
    account_positions = relationship(
        "AccountPosition", back_populates="account", cascade="all, delete, delete-orphan"
    )

    def as_dict(self):
        result = {'id': self.id, 'account_number': self.account_number,
                  'broker_name': self.broker_name, 'portfolio_id': self.portfolio_id}
        return result


class AccountPosition(Base):
    __tablename__ = 'account_positions'
    __table_args__ = (
        UniqueConstraint("account_id", "symbol", name="account_positions_account_id_symbol_key"),
    )
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account_number = Column(String, nullable=False)
    broker_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    account = relationship("Account", back_populates="account_positions")
    portfolio = relationship("Portfolio", back_populates="account_positions")

    def as_dict(self):
        return (
            {'id': self.id, 'portfolio_id': self.portfolio_id, 'account_id': self.account_id,
             'broker_name': self.broker_name, 'account_number': self.account_number,
             'symbol': self.symbol, 'shares': str(self.shares)})


class AccountPositionPrice(Base):
    __tablename__ = 'account_position_price'
    id = Column(Integer, primary_key=True)
    account_position_id = Column(Integer, ForeignKey('account_positions.id'), nullable=False)
    business_price_id = Column(Integer, ForeignKey('business_price.id'), nullable=False)
