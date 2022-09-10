from flask import Blueprint
from flask_restx import Api
from flask_cors import cross_origin

api_blueprint = Blueprint("api", __name__)
api_v1 = Api(api_blueprint, doc="/docs", decorators=[cross_origin()])

from .auth.router import auth

api_v1.add_namespace(auth)

from .account.router import account

api_v1.add_namespace(account)

from .admin.router import admin

api_v1.add_namespace(admin)

from .business.router import business

api_v1.add_namespace(business)

from .model.router import model

api_v1.add_namespace(model)

from .portfolio.router import portfolio

api_v1.add_namespace(portfolio)

from .trade.router import trade

api_v1.add_namespace(trade)

from .user.router import user

api_v1.add_namespace(user)
