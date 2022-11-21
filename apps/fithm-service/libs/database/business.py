from libs.database import db_session
from apps.model.models import ModelPosition
from apps.account.models import AccountPosition
from apps.business.models import BusinessPrice


def remove_free_business_prices(business_id: int):
    account_symbols = db_session.query(AccountPosition.symbol).all()
    model_symbols = db_session.query(ModelPosition.symbol).all()
    symbols = list(set([*account_symbols, *model_symbols]))
    symbols = [sym[0] for sym in symbols]

    db_session.query(BusinessPrice).filter(
        BusinessPrice.business_id == business_id,
        BusinessPrice.symbol.notin_(symbols)
    ).delete()

    db_session.commit()
