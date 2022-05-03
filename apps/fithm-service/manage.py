from flask.cli import FlaskGroup, AppGroup
from libs.database import create_tables, drop_tables, populate_default
from main import create_app

db_cli = AppGroup('db')


@db_cli.command('create')
def create_db():
    create_tables()
    populate_default()


@db_cli.command('drop')
def drop_db():
    drop_tables()

create_app().cli.add_command(db_cli)
