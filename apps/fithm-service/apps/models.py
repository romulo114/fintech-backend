from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Integer,
    DateTime,
    Boolean
)
from sqlalchemy.orm import relationship
from libs.database import Base

from apps.account.models import Account, AccountPosition
from apps.model.models import Model, ModelPosition
from apps.portfolio.models import Portfolio
from apps.trade.models import Trade, TradeRequest
from apps.business.models import Business

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    account_position_id = Column(Integer, ForeignKey('account_positions.id'))
    model_position_id = Column(Integer, ForeignKey('model_positions.id'))
    trade_id = Column(Integer, ForeignKey('trades.id'))
    symbol = Column(String, nullable=False)
    price = Column(Float)
    trade = relationship("Trade", back_populates="prices")
    model_position = relationship(
        "ModelPosition", back_populates="trade_prices")
    account_position = relationship(
        "AccountPosition", back_populates="trade_prices")

    def as_dict(self):
        return {'id': self.id, 'trade_id': self.trade_id, 'symbol': self.symbol, 'price': str(self.price)}
