from flask import Flask
from flask_mail import Mail
from sqlalchemy import create_engine

from config import Config
from libs.database import db_session, init_db, create_tables
from libs.middleware import init_middlewares
from libs.depends.register import register_all

# from settings import SERVICE_DB_URL

# engine = create_engine(
#     SERVICE_DB_URL,
#     convert_unicode=True,
#     max_overflow=100
# )
# db_session.configure(bind=engine)


def create_app(service_db_url=None):

    engine = create_engine(
        service_db_url,
        convert_unicode=True,
        max_overflow=100)
    db_session.configure(bind=engine)

    """App factory function"""
    from settings import registered
    app = Flask(__name__)
    app.config_class = Config
    Mail(app)
    init_db(app, db_session)
    init_middlewares(app)
    create_tables(engine)

    from apps.api_v1 import api_blueprint as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    return app


