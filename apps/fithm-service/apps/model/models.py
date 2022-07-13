from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    Integer,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from apps.business.models import BusinessPrice
from libs.database import Base, Stateful, db_session


class Model(Stateful):
    """Model table"""

    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    name = Column(String)
    description = Column(String)
    keywords = Column("data", postgresql.ARRAY(String))
    is_public = Column(Boolean, default=False, nullable=False)
    business = relationship("Business", back_populates="models")
    allocation = relationship(
        "ModelPosition", back_populates="model", cascade="all, delete, delete-orphan"
    )
    portfolio = relationship("Portfolio", back_populates="model")

    def as_dict(self):
        result = {
            "id": self.id,
            "name": self.name,
            "keywords": [],
            "is_public": self.is_public,
            "description": self.description,
        }
        if self.allocation:
            result["positions"] = [a.as_dict() for a in self.allocation]
        if self.keywords:
            result["keywords"] = [k for k in self.keywords]
        return result


class ModelPosition(Base):
    __tablename__ = "model_positions"
    __table_args__ = (
        UniqueConstraint(
            "model_id", "symbol", name="model_positions_model_id_symbol_key"
        ),
    )
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    symbol = Column(String)
    weight = Column(Float)
    model = relationship("Model", back_populates="allocation")

    def as_dict(self):
        result = {
            "model_id": self.model_id,
            "symbol": self.symbol,
            "weight": self.weight,
        }
        return result


class ModelPositionPrice(Base):
    __tablename__ = "model_position_price"
    id = Column(Integer, primary_key=True)
    model_position_id = Column(
        Integer, ForeignKey("model_positions.id"), nullable=False
    )
    business_price_id = Column(Integer, ForeignKey("business_price.id"), nullable=False)
    model_position = relationship(
        "ModelPosition", back_populates="model_position_price"
    )
    price = relationship("BusinessPrice", back_populates="account_position_prices")

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
