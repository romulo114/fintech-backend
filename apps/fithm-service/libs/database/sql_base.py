from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import Base
import apps.models

service_db_url = "postgresql+psycopg2://ryeland:11111111@postgres:5432/service"

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False)
)

engine = create_engine(
    service_db_url,
    convert_unicode=True,
    max_overflow=100)
Base.metadata.create_all(bind=engine)
db_session.configure(bind=engine)