from libs.database.defaults import default_values, clear_db_data
from apps.business.models import Business


def test_create_clear_defaults(db_session):
    default_values(db_session)
    clear_db_data(db_session)
