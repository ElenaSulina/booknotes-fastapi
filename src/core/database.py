from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import config


db_uri = config.assemble_database_uri()
engine = create_engine(db_uri, echo=False)


class Base(DeclarativeBase):
    pass


# def create_tables():
#     Base.metadata.create_all(engine)


session_factory = sessionmaker(engine)


def create_session():
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
