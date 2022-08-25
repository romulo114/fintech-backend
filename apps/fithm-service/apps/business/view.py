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


    def create_business(self, body: dict) -> dict:
        """Create a new business for the user"""

        # check existence
        business = db_session.query(Business).filter(Business.id == g.business_id).all()
        if len(business):
            abort(403, "Business already exists")

        # create an business
        business = Business(
            id=g.business_id,
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


    def update_business(self, id: int, body: dict) -> dict:
        """Update an existing business"""

        business = self.__get_business(id)
        if "business_number" in body:
            business.business_number = body["business_number"]
        if "broker_name" in body:
            business.broker_name = body["broker_name"]

        db_session.commit()
        return business.as_dict()


    def delete_business(self, id: int):
        """Delete an business"""

        business = self.__get_business(id)
        db_session.delete(business)
        db_session.commit()

        return {"result": "success"}


    def get_business_prices(self, id: int):
        """Get related prices"""

        prices: list[BusinessPrice] = db_session.query(BusinessPrice).filter(BusinessPrice.business_id == id).all()
        return [
            price.as_dict() for price in prices
        ]


    def __get_business(self, id: int) -> Business:

        business = db_session.query(Business).get(id)
        if not business:
            abort(404, "Business not found")
        if business.id != g.business.id:
            abort(403, "You don't have permission to this business.")

        return business
