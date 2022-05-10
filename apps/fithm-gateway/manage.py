import click

from flask import Flask
from flask.cli import AppGroup
from sqlalchemy import create_engine

from libs.database import create_tables, drop_tables, populate_default, db_session
from settings import GATEWAY_DB_URL

engine = create_engine(
    GATEWAY_DB_URL,
    convert_unicode=True,
    max_overflow=100,
)
db_session.configure(bind=engine)

app = Flask(__name__)

db_cli = AppGroup('db')


@db_cli.command('create')
def create_db():
    create_tables(engine)
    populate_default(db_session)


@db_cli.command('drop')
def drop_db():
    drop_tables()


app.cli.add_command(db_cli)
