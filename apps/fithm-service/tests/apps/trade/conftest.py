import datetime as dt
from pytest import fixture

@fixture
def trade(db_session, business):
    from apps.trade.models import Trade
    trade = Trade(business_id=business.id, name="test_trade", created=dt.datetime.utcnow(), status='active')
    db_session.add(trade)
    db_session.commit()
    return trade


@fixture
def trade_portfolios(db_session, trade):
    pass