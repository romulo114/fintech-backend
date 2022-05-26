from functools import wraps
from flask import current_app, g, request
from flask.app import Flask
from libs.database import db_session
from apps.models import Business
from urllib3.exceptions import HTTPError


def init_middlewares(app: Flask):
    '''Initialize app with middlewares'''

    @app.before_request
    def user_middleware():
        '''User middleware'''

        current_app.logger.debug(f'request params: {request.args}')
        current_app.logger.debug(f'request body: {request.json}')
        if request.method == 'GET' or request.method == 'DELETE':
            business_id = request.args['business_id'] if 'business_id' in request.args else None
        else:
            business_id = request.json['business_id'] if 'business_id' in request.json else None

        business: Business = db_session.query(Business).filter(Business.id == business_id).first()
        if not business:
            if not getattr(request, "json"):
                raise HTTPError()
            if request.json["create_business"]:
                g.business_id = business_id
                return
        g.business = business
        if g.business:
            current_app.logger.debug(f'requesting business id: {g.business.id}')
