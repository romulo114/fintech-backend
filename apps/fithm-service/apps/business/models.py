from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Float
)
from sqlalchemy.orm import relationship
from libs.database import Base, Stateful


class Business(Base):
    '''User business'''

    __tablename__ = 'business'

    id = Column(Integer, primary_key=True)
    models = relationship("Model", back_populates="business", cascade="all, delete, delete-orphan")
    portfolios = relationship("Portfolio", back_populates="business", cascade="all, delete, delete-orphan")
    trades = relationship("Trade", back_populates="business", cascade="all, delete, delete-orphan")
    accounts = relationship("Account", back_populates="business", cascade="all, delete, delete-orphan")

    def as_dict(self):
        return ({'id': self.id})
