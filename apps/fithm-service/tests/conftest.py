import testing.postgresql

from pytest import fixture

from main import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from apps.account.models import Account

@fixture
def engine():
    return create_engine(
    "postgres://localhost/test_database")


@fixture(scope="session")
def tables(engine):


db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


@fixture
def app():
    app = create_app()
    app.testing = True
    return app
