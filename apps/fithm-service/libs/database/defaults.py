import csv

import datetime as dt

from apps.model.models import Model
from apps.account.models import Account
from apps.business.models import Business
from apps.portfolio.models import Portfolio
from apps.trade.models import Trade

from libs.depends.register import container


def default_values(db_session):
    '''Populate default values'''
    # add business
    with open("scripts/fixtures/businesses.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            business = db_session.query(Business).filter(Business.id == row["id"]).first()
            if not business:
                db_session.add(Business())
    db_session.commit()
    with open("scripts/fixtures/models.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            models = db_session.query(Model).filter(Model.business_id == row["business_id"]).all()
            if not models:
                row["active"] = True if row["active"] == "true" else False
                row["is_public"] = True if row["is_public"] == "true" else False
                db_session.add(Model(**row))
    db_session.commit()
    with open("scripts/fixtures/portfolios.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            portfolios = db_session.query(Portfolio).filter(Portfolio.business_id == row["business_id"]).all()
            if not portfolios:
                row["active"] = True if row["active"] == "true" else False
                db_session.add(Portfolio(**row))
    db_session.commit()
    with open("scripts/fixtures/accounts.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts = db_session.query(Account).filter(Account.business_id == row["business_id"]).all()
            if not accounts:
                row["active"] = True if row["active"] == "True" else False
                db_session.add(Account(**row))
    db_session.commit()
    with open("scripts/fixtures/trades.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            trades = db_session.query(Trade).filter(Trade.business_id == row["business_id"]).all()
            if not trades:
                row["status"] = "active"
                row["created"] = dt.datetime.now()
                db_session.add(Trade(**row))
    db_session.commit()


def clear_db_data(db_session):
    trades = db_session.query(Trade).all()
    [db_session.delete(trade) for trade in trades]
    accounts = db_session.query(Account).all()
    [db_session.delete(account) for account in accounts]
    portfolios = db_session.query(Portfolio).all()
    [db_session.delete(model) for model in portfolios]
    models = db_session.query(Model).all()
    [db_session.delete(model) for model in models]
    businesses = db_session.query(Business).all()
    [db_session.delete(business) for business in businesses]
    db_session.commit()