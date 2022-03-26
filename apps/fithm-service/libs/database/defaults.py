from apps.model.models import Model
from apps.account.models import Account
from apps.portfolio.models import Portfolio
from libs.database import db_session
from libs.depends.register import container


def default_values():
    '''Populate default values'''

    # add account
    account = Account(business_id=1, account_number=1, broker_name="Test Broker", )

    db_session.add(account)

    # add admin user
    db_session.commit()