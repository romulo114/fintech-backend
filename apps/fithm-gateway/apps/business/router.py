from flask_restx import Namespace, Resource
from flask import request, current_app
from libs.depends.entry import container
from libs.helper.forward import forward_request
from libs.middleware.auth import login_required, active_required
from .lib.parser import BusinessParser

business = Namespace(
    "business", path="/business", decorators=[active_required(), login_required()]
)


@business.route("")
class Businesses(Resource):
    @business.doc("get businesses")
    def get(self):
        """List all businesses"""

        return forward_request()


    @business.doc("create business")
    def post(self):
        """Create a business for a user"""

        return forward_request()


@business.route("/<int:business_id>")
class Business(Resource):
    @business.doc("get business info")
    def get(self, business_id: str):

        return forward_request()

    @business.doc("delete business")
    def delete(self, business_id: str):
        """Update an existing account"""

        return forward_request()


@business.route("/prices")
class BusinessPrices(Resource):
    @business.doc("get prices")
    def get(self):

        return forward_request()


    @business.doc("create a business price")
    def post(self):
        """Create a business price"""

        parser: BusinessParser = container.get(BusinessParser)
        param = parser.parse_price_create(request)

        return forward_request(body=param)


@business.route(("/prices/<int:business_price_id>"))
class BusinessPrice(Resource):

    @business.doc("update an existing business price")
    def put(self, business_price_id: int):

        parser: BusinessParser = container.get(BusinessParser)
        param = parser.parse_price_create(request)

        return forward_request(body=param)


    @business.doc("delete an existing business price")
    def delete(self, business_price_id: int):
        
        return forward_request()
