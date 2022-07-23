import datetime as dt
from pytest import fixture

from apps.trade.models import Trade, TradePortfolio

@fixture
def trade(db_session, business, portfolio):

    trade = Trade(
        name="test_trade_from_heee",
        business_id=business.id,
        created=dt.datetime.now(),
        status='active',
    )
    db_session.add(trade)
    db_session.commit()
    trade_portfolio = TradePortfolio(
        portfolio_id=portfolio.id,
        trade_id=trade.id,
        active=True,
    )
    db_session.add(trade_portfolio)
    db_session.commit()
    return trade


@fixture
def trade_with_portfolios_accounts(db_session, business, portfolio_account_account_position):
    trade = Trade(
        name="test_trade_heheh",
        business_id=business.id,
        created=dt.datetime.now(),
        status='active',
    )
    db_session.add(trade)
    db_session.flush()
    trade_portfolio = TradePortfolio(
        portfolio_id=portfolio_account_account_position.id,
        trade_id=trade.id,
        active=True,
    )
    db_session.add(trade_portfolio)
    db_session.commit()
    return trade