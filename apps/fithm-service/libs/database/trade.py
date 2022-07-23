from flask import current_app
from libs.database import db_session
from .portfolios import get_portfolios
from apps.account.models import Account, AccountPosition
from apps.business.models import Business
from apps.model.models import Model
from apps.portfolio.models import Portfolio
from apps.trade.models import Trade

import pandas as pd
from iexfinance.stocks import Stock
from datetime import datetime


def get_trade_prices(trade: Trade, use: str = 'read'):

    prices = trade.prices
    if len(prices) == 0:
        return None
    df_prices = pd.DataFrame(prices)
    df_prices.columns = ['price_object']
    df_price_details = pd.DataFrame([vars(p) for p in prices])
    if use == "read":
        obj_detail = pd.concat([df_prices, df_price_details], axis=1).drop_duplicates(
            subset=['symbol']
        )
    else:
        obj_detail = pd.concat([df_prices, df_price_details], axis=1)

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(obj_detail)
    return obj_detail


def update_trade_prices(trade: Trade, prices = None):

    if prices is None:
        prices = get_iex(trade)
    price_unique = [dict(t) for t in {tuple(d.items()) for d in prices}]
    ext_symbols = list(set([a['symbol'] for a in prices]))
    if len(price_unique) != len(ext_symbols):
        return 'You have attempted to use different prices for the same security.'

    current_prices = get_trade_prices(trade, use="write")

    df_price_unique = pd.DataFrame(price_unique).set_index(['symbol'])
    current_prices = current_prices[
        current_prices['symbol'].isin([p['symbol'] for p in price_unique])
    ].drop('price', axis=1).set_index(['symbol'])
    current_prices['new_price'] = df_price_unique['price']

    def assign_it(row):
        row['price_object'].price = row['new_price']

    current_prices.apply(assign_it, axis=1)
    db_session.bulk_save_objects(current_prices['price_object'].tolist())
    db_session.commit()


def get_trade_instructions(trade: Trade):
    # get all symbols from all models in trade

    portfolios = trade.active_portfolios.all()

    account_position_headers, account_positions = trade.get_trade_positions()
    if any([True if p.model_id is None else False for p in portfolios]):
        return ValueError('One of your portfolios has not been assigned a model.')
    # add portfolio_id to each model position
    model_position_headers, model_positions = trade.get_model_positions()
    df_model_positions = pd.DataFrame(model_positions, columns=model_position_headers).set_index(['portfolio_id'], inplace=True)

    df_account_positions = pd.DataFrame(account_positions, columns=account_position_headers).set_index(['portfolio_id'], inplace=True)

    # df_all_positions = pd.concat([df_model_positions, df_account_positions])
    # df_all_positions.set_index(['symbol'], inplace=True)

    price_headers, prices = trade.get_prices()
    df_prices = pd.DataFrame(prices, columns=price_headers)

    #.drop_duplicates(inplace=True).set_index(["symbol"], inplace=True)
    print(df_prices)
    return
    df_all_positions['price'] = df_prices['price']
    df_all_positions['restrictions'] = float('NaN')
    df_all_positions['trade_id'] = trade.id
    df_all_positions.rename(columns={'weight': 'model_weight'}, inplace=True)
    df_all_positions.reset_index(inplace=True)
    df_all_positions.account_number.fillna('model', inplace=True)

    all_requests = []
    for i, port in df_all_positions.groupby('portfolio_id'):
        trade_request_obj = {'portfolio_id': i}
        trade_request_obj['portfolio'] = df_all_positions.loc[:,
            ['account_number', 'symbol', 'shares', 'model_weight', 'price', 'restrictions']
        ].to_dict('list')
        all_requests.append(trade_request_obj)
    if 'send' in args:
        df_all_positions['archive'] = df_all_positions.apply(
            lambda row: TradeRequest(
                created=datetime.utcnow(),
                trade_id=trade.id,
                portfolio_id=row['portfolio_id'],
                account_id=row['account_id'],
                account_number=row['account_number'],
                broker_name=row['broker_name'],
                symbol=row['symbol'],
                shares=row['shares'],
                model_weight=row['model_weight'],
                price=row['price'],
                restrictions=float('NaN')), axis=1)
        db_session.bulk_save_objects(df_all_positions.archive.tolist())
        db_session.commit()
        all_trades = []
        for t in all_requests:
            trade_manager = TradeManager('json', t['portfolio'])
            all_trades.append(trade_manager.trade_instructions.to_dict(orient='records'))
        return all_trades
    else:
        return all_requests


def get_iex(trade: Trade):

    current = trade.get_prices()
    account_cash = current.loc[current == 'account_cash'].any()
    current = current.loc[current != 'account_cash']

    if current.empty:
        if account_cash:
            return [{'price': 1, 'symbol': 'account_cash'}]
        return []

    batch = Stock(current.tolist())
    prices = batch.get_price()
    if type(prices) == float:
        result = [{'symbol': current.tolist()[0], 'price': prices}]
    else:
        result = [{'price': v, 'symbol': i} for i, v in prices.items()]

    if account_cash:
        result.append({'price': 1, 'symbol': 'account_cash'})

    return result