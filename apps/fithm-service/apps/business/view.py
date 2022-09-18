from datetime import datetime
from typing import List
from flask import current_app, g, abort
from libs.database import db_session
from .models import Business, BusinessPrice


class BusinessView:
    def __init__(self):
        pass


    def get_businesses(self):
        """Get all businesses owned by user"""

        business: Business = g.business
        businesses: List[Business] = business.businesses
        return {
            "businesses": [
                business.as_dict() for business in businesses if business.active
            ]
        }


    def create_business(self) -> dict:
        """Create a new business for the user"""

        # check existence
        business = db_session.query(Business).filter(Business.id == g.business_id).all()
        if len(business):
            abort(403, "Business already exists")

        # create an business
        business = Business(
            id=g.business_id
        )

        db_session.add(business)
        db_session.commit()

        return business.as_dict()


    def get_business(self, id: int):
        """Get business detail"""

        business = self.__get_business(id)
        # if not business.active:
        #     abort(401, 'Not active business')

        return business.as_dict()


    def delete_business(self, id: int):
        """Delete an business"""

        business = self.__get_business(id)
        db_session.delete(business)
        db_session.commit()

        return {"result": "success"}


    def get_business_prices(self):
        """Get related prices"""

        business_id = g.business.id
        current_app.logger.info(f'business_id = {business_id}')
        try:
            prices: list[BusinessPrice] = db_session.query(BusinessPrice).filter(BusinessPrice.business_id == business_id).all()
        except Exception:
            prices: list[BusinessPrice] = []
        return [
            price.as_dict() for price in prices
        ]


    def create_business_price(self, body: dict):
        """Create a business price"""

        symbol = body["symbol"] if "symbol" in body else None
        price = body["price"] if "price" in body else 0
        if symbol is None:
            abort(400, "symbol must be specified")

        business_id = g.business.id
        business_price: BusinessPrice = BusinessPrice(
            business_id=business_id,
            symbol=symbol,
            price=price,
            updated=datetime.utcnow()
        )

        db_session.add(business_price)
        db_session.commit()

        return business_price.as_dict()


    def update_business_price(self, price_id: int, body: dict):
        """Update an existing price"""

        business_price: BusinessPrice = db_session.query(BusinessPrice).get(price_id)
        if not business_price:
            abort(404, "Business price not found")

        if "symbol" in body:
            business_price.symbol = body["symbol"]
        if "price" in body:
            business_price.price = body["price"]
        db_session.commit()

        return business_price.as_dict()


    def delete_business_price(self, price_id):
        """Delete an existing price"""

        business_price: BusinessPrice = db_session.query(BusinessPrice).get(price_id)
        if business_price is not None:
            account_position_prices = business_price.account_position_prices
            if account_position_prices:
                for price in account_position_prices:
                    db_session.delete(price.account_position)
                    db_session.delete(price)
            db_session.delete(business_price)
            db_session.commit()

        return { "result": "success" }


    def __get_business(self, id: int) -> Business:

        business = db_session.query(Business).get(id)
        if not business:
            abort(404, "Business not found")
        if business.id != g.business.id:
            abort(403, "You don't have permission to this business.")

        return business
