from flask import Flask

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False)
)


Base = declarative_base()


class Stateful(Base):
    __abstract__ = True
    active = Column(Boolean(), nullable=False, default=True)


def init_db(app: Flask, session):
    """Initialize the database and flask app"""

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()


def create_tables(engine):
    import apps.models
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)


def populate_default(engine):
    from .defaults import default_values
    db_session.configure(bind=engine)
    default_values(db_session)


def drop_tables(engine):
    import apps.models
    Base.metadata.drop_all(engine)

