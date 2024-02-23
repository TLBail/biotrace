from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

engine = None
db_session = scoped_session(lambda: create_session(bind=engine))

Base = declarative_base()


def init_engine(uri, **kwargs):
	global engine
	engine = create_engine(uri, **kwargs)
	if not database_exists(engine.url):
		create_database(engine.url)
	return engine


def init_db():
	from models import File  # noqa: F401
	Base.metadata.create_all(bind=engine)
