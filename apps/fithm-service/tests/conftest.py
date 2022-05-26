import os
import pytest
import requests
import requests_mock

from flask import Flask
from pytest import fixture

from pytest_postgresql import factories
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from main import create_app

postgresql_in_docker = factories.postgresql_noproc(
    user="ryeland", host="postgres", dbname="test", password="11111111"
)
postgresql = factories.postgresql("postgresql_in_docker")


@pytest.fixture
def connection(postgresql):
    return f"postgresql+psycopg2://{postgresql.info.user}:{postgresql.info.password}" \
                 f"@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"


@pytest.fixture
def engine(connection):
    return create_engine(connection, convert_unicode=True, max_overflow=100)


@pytest.fixture
def db_session(engine):
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    from libs.database import init_db, create_tables, Base

    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    create_tables(engine)
    yield db_session


# def init_db(app: Flask, db_session):
#     """Initialize the database and flask app"""
#
#     @app.teardown_appcontext
#     def shutdown_session(exception=None):
#         db_session.remove()


@pytest.fixture
def app(connection):
    app = create_app(service_db_url=connection)
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

@pytest.fixture
def business(db_session):
    from apps.business.models import Business
    business = Business(id=1)
    db_session.add(business)
    db_session.commit()