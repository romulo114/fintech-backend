import os
import pytest
import requests
import requests_mock

from flask import Flask
from pytest import fixture

# from pytest_postgresql import factories

from apps.auth.view import AuthView
from apps.models import User
from libs.database import db_session
from main import create_app
GATEWAY_DB_URL =f'postgresql+psycopg2://ryeland:11111111@postgres:5432/gateway'


# postgresql_in_docker = factories.postgresql_noproc(
#     user="ryeland", host="postgres", dbname="test", password="11111111"
# )
# postgresql = factories.postgresql("postgresql_in_docker")
#
# @pytest.fixture
# def engine(postgresql):
#     connection = f"postgresql+psycopg2://{postgresql.info.user}:{postgresql.info.password}" \
#                  f"@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
#     return create_engine(connection, convert_unicode=True, max_overflow=100)

# @pytest.fixture
# def db_session(engine):
#     db_session = scoped_session(
#         sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     )
#
#     from libs.database import init_db, create_tables, Base
#
#     Base.query = db_session.query_property()
#     Base.metadata.create_all(bind=engine)
#     create_tables(engine)
#     yield db_session


# def init_db(app: Flask, db_session):
#     """Initialize the database and flask app"""
#
#     @app.teardown_appcontext
#     def shutdown_session(exception=None):
#         db_session.remove()
from sqlalchemy import create_engine


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@fixture
def session():
    engine = create_engine(
        GATEWAY_DB_URL,
        convert_unicode=True,
        max_overflow=100
    )
    db_session.configure(bind=engine)

@fixture
def create_user(session):
    return db_session.query(User).filter(User.email=="test@test.com").one()

@fixture
def token(app, create_user):
    with app.app_context():
        auth_view = AuthView()

        return auth_view.signin(create_user.email, "password")

@fixture
def teardown_user(session):
    user = db_session.query(User).filter(User.email=="test@test.com").one()
    db_session.delete(user)
    db_session.commit()