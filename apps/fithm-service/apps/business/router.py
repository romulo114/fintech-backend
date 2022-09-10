from flask_restx import Namespace, Resource
from flask import request
from .view import BusinessView

business = Namespace("business", path="/business")
view = BusinessView()


@business.route("")
class Businesses(Resource):
    @business.doc("get businesses")
    def get(self):
        """List all businesses"""

        return view.get_businesses()

    @business.doc("create business")
    def post(self):
        """Create a business for a user"""

        return view.create_business(request.json)


@business.route("/<int:business_id>")
class Business(Resource):
    @business.doc("get business info")
    def get(self, business_id: int):

        return view.get_business(business_id)

    @business.doc("update business info")
    def put(self, business_id: int):

        return view.update_business(business_id, request.json)

    @business.doc("delete business")
    def delete(self, business_id: int):

        return view.delete_business(business_id)


@business.route("/<int:business_id>/prices")
class BusinessPrice(Resource):
    @business.doc("get prices")
    def get(self, business_id: int):

        return view.get_business_prices(business_id)


    @business.doc("create a business price")
    def post(self, business_id: int):

        return view.create_business_price(business_id, request.json)


    @business.doc("update an existing business price")
    def put(self, business_price_id: int):

        return view.update_business_price(business_price_id, request.json)


    @business.doc("delete an existing business price")
    def put(self, business_price_id: int):
        
        return view.delete_business_price(business_price_id)
