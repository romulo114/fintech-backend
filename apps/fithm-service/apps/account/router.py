from flask_restx import Namespace, Resource
from flask import request
from .view import AccountView, AccountPositionView

account = Namespace("account", path="/accounts")
view = AccountView()
account_position_view = AccountPositionView()


@account.route("")
class Accounts(Resource):
    @account.doc("get accounts")
    def get(self):
        """List all accounts"""

        return view.get_accounts()

    @account.doc("create account")
    def post(self):
        """Create an account for a business"""

        return view.create_account(request.json)


@account.route("/<int:account_id>")
class Account(Resource):
    @account.doc("get account info")
    def get(self, account_id: str):

        return view.get_account(account_id)


    @account.doc("update account info")
    def put(self, account_id: str):

        return view.update_account(account_id, request.json)


    @account.doc("delete account")
    def delete(self, account_id: str):

        return view.delete_account(account_id)


@account.route("/<int:account_id>/positions")
class AccountPosition(Resource):
    @account.doc("get account positions")
    def get(self, account_id: int):

        return account_position_view.get_positions(account_id)


    @account.doc("create account positions")
    def post(self, account_id: int):

        return account_position_view.create_position(account_id, request.json)


    @account.doc("update account positions")
    def put(self, account_id: int):

        return account_position_view.update_positions(account_id, request.json)
