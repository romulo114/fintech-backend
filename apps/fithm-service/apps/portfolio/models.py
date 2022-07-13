from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from libs.database import Base, Stateful


class Portfolio(Stateful):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("business.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"))
    name = Column(String)
    business = relationship("Business", back_populates="portfolios")
    accounts = relationship("Account", back_populates="portfolio")
    model = relationship("Model", uselist=False, back_populates="portfolio")
    trades = relationship(
        "TradePortfolio",
        back_populates="portfolio",
        cascade="all, delete, delete-orphan",
    )

    def as_dict(self, include_account_positions=False):
        result = {
            "id": self.id,
            "name": self.name,
            "model": None,
            "accounts": [],
        }
        if self.accounts:
            result["accounts"] = [
                a.as_dict(include_account_positions) for a in self.accounts
            ]
            result["has_prices"] = all([all(
                [account.has_prices for account in self.accounts]
            ), self.model.has_price])
            result["has_cash_positions"] = all(
                [account.has_cash_position for account in self.accounts]
            )
        if self.model:
            result["model"] = self.model.as_dict()
        return result
