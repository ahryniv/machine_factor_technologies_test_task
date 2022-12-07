import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.conf.settings import settings


engine = sa.create_engine(settings.sqlalchemy_database_uri)
metadata = sa.MetaData(bind=engine)

Base = declarative_base(metadata=metadata)
DBSession = sessionmaker(engine)


class BaseModelID(Base):
    __abstract__ = True

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
