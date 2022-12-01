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

    @property
    def has_prices(self):
        has_price = True
        if self.accounts:
            has_price = has_price and all([account.has_prices for account in self.accounts])
        if self.model:
            has_price = has_price and self.model.has_prices

        return has_price


    @property
    def has_cash_positions(self):
        return all([account.has_cash_position for account in self.accounts])

    def get_account_positions(self):
        positions = [["portfolio_id", "account_number", "symbol", "shares"]]
        for account in self.accounts:
            for account_position in account.account_positions:
                positions.append(
                    [
                        self.id,
                        account_position.account_number,
                        account_position.symbol,
                        account_position.shares,
                    ]
                )

        return positions

    def get_model_positions(self):
        positions = []
        for model_position in self.model_positions:
            self.append(model_position)
        return positions

    def as_dict(self, include_account_positions=False, include_model_positions=False):
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
            result["has_prices"] = self.has_prices
            result["has_cash_positions"] = self.has_cash_positions
        if self.model:
            result["model"] = self.model.as_dict(include_model_positions)
        return result
