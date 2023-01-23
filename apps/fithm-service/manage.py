import click
from flask import Flask
from flask.cli import AppGroup
from sqlalchemy import create_engine, inspect

from libs.database import create_tables, drop_tables, populate_default, db_session, remove_default
from settings import SERVICE_DB_URL

engine = create_engine(
    SERVICE_DB_URL,
    convert_unicode=True,
    max_overflow=100,
)
db_session.configure(bind=engine)

app = Flask(__name__)

db_cli = AppGroup('db')


@db_cli.command('create')
def create_db():
    inspector = inspect(engine)
    if inspector.has_table('business'):
        return

    create_tables(engine)
    populate_default(engine)


@db_cli.command('populate')
def populate_db():
    populate_default(engine)


@db_cli.command('clear')
def clear_db():
    remove_default(engine)


@db_cli.command('drop')
def drop_db():
    drop_tables(engine)


app.cli.add_command(db_cli)