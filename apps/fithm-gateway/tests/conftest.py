import pytest
from flask import Flask
from flask_cors import CORS
from pytest import fixture

from pytest_postgresql import factories
from sqlalchemy import create_engine

from libs.database import init_db
from libs.middleware.auth import init_middlewares
from main import create_app
from config import Config
from sqlalchemy.orm import scoped_session, sessionmaker

postgresql_in_docker = factories.postgresql_noproc(user="ryeland", host="postgres", dbname="test", password="11111111")
postgresql = factories.postgresql("postgresql_in_docker")

@pytest.fixture
def db_session(postgresql):
    connection = f'postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}'
    engine = create_engine(
        connection,
        convert_unicode=True,
        max_overflow=100
    )
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return db_session

def init_db(app: Flask, db_seesion):
    """Initialize the database and flask app"""

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

@fixture
def app(db_session):
    app = Flask(__name__)
    app.config.from_object(Config())
    app.testing = True
    init_db(app, db_session)
    from apps.api_v1 import api_blueprint as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    CORS(app)
    init_middlewares(app)
    return app
