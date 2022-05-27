import datetime
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
    return (
        f"postgresql+psycopg2://{postgresql.info.user}:{postgresql.info.password}"
        f"@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
    )


@pytest.fixture
def engine(connection):
    return create_engine(connection, convert_unicode=True, max_overflow=100)


@pytest.fixture
def db_session(engine):
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    from libs.database import create_tables, Base

    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    create_tables(engine)
    yield db_session
    db_session.commit()
    Base.metadata.drop_all(engine)


# def init_db(app: Flask, db_session):
#     """Initialize the database and flask app"""
#
#     @app.teardown_appcontext
#     def shutdown_session(exception=None):
#         db_session.remove()


@pytest.fixture
def app(connection):
    app = create_app(service_db_url=connection)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def business(db_session):
    from apps.business.models import Business

    business = Business()
    db_session.add(business)
    db_session.commit()
    return business


@pytest.fixture
def account(db_session, business):
    from apps.account.models import Account

    account = Account(
        business_id=business.id, account_number="888", broker_name="test broker"
    )
    db_session.add(account)
    db_session.commit()
    return account


@pytest.fixture
def model(db_session, business):
    from apps.model.models import Model

    model = Model(business_id=business.id)
    db_session.add(model)
    db_session.commit()
    return model


@pytest.fixture
def portfolio(db_session, business):
    from apps.portfolio.models import Portfolio

    portfolio = Portfolio(business_id=business.id)
    db_session.add(portfolio)
    db_session.commit()
    return portfolio


@pytest.fixture
def trade(db_session, business):
    from apps.trade.models import Trade

    trade = Trade(business_id=business.id, name="test_trade", created=datetime.datetime.utcnow(), status=False)
    db_session.add(trade)
    db_session.commit()
    return trade
