from apps.model.models import Model
from apps.account.models import Account
from apps.business.models import Business
from apps.portfolio.models import Portfolio

from libs.depends.register import container


def default_values(db_session):
    '''Populate default values'''
    # add business
    business = db_session.query(Business).filter(Business.id==1).first()
    if business:
        return
    db_session.add(Business(id=1))

    # add account
    account = Account(business_id=1, account_number=1, broker_name="Test Broker", )

    db_session.add(account)

    # add admin user
    db_session.commit()