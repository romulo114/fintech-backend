from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from sqlalchemy import create_engine
from config import Config
from settings import GATEWAY_DB_URL


from libs.database import init_db, db_session
from libs.middleware.auth import init_middlewares
from libs.email.message import init_mail

engine = create_engine(
    GATEWAY_DB_URL,
    convert_unicode=True,
    max_overflow=100
)
db_session.configure(bind=engine)

def create_app():
    """App factory function"""
    from settings import registered
    app = Flask(__name__)
    app.config.from_object(Config())

    init_mail(app)
    init_db(app, db_session)

    from apps.api_v1 import api_blueprint as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    CORS(app)
    init_middlewares(app)
    return app