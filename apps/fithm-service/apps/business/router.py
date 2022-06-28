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
    def get(self, business_id: str):

        return view.get_business(business_id)

    @business.doc("update business info")
    def put(self, business_id: str):

        return view.update_business(business_id, request.json)

    @business.doc("delete business")
    def delete(self, business_id: str):

        return view.delete_account(business_id)
