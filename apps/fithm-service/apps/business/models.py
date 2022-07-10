from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Float,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from libs.database import Base, Stateful


class Business(Base):
    """User business"""

    __tablename__ = "business"

    id = Column(Integer, primary_key=True)
    models = relationship(
        "Model", back_populates="business", cascade="all, delete, delete-orphan"
    )
    portfolios = relationship(
        "Portfolio", back_populates="business", cascade="all, delete, delete-orphan"
    )
    trades = relationship(
        "Trade", back_populates="business", cascade="all, delete, delete-orphan"
    )
    accounts = relationship(
        "Account", back_populates="business", cascade="all, delete, delete-orphan"
    )

    def as_dict(self):
        return {"id": self.id}


class BusinessPrice(Base):
    """Security Prices per business"""

    __tablename__ = "business_price"
    __table_args__ = (
        UniqueConstraint("business_id", "symbol", name="business_security_price"),
    )

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    symbol = Column(String, nullable=False)
    price = Column(Float)
    updated = Column(DateTime, nullable=False)
    account_position_prices = relationship("AccountPositionPrice", back_populates="price")

    def as_dict(self):
        return {"id": self.id}
