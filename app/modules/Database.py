from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy_utils import database_exists, create_database
from models.File import File
from models.Base import Base

engine = None
db_session = scoped_session(lambda: create_session(bind=engine))  # type: ignore
db_models = {}
db_models['File'] = File


def init_engine(uri, **kwargs):
	global engine
	engine = create_engine(uri, **kwargs)
	if not database_exists(engine.url):
		create_database(engine.url)
	return engine


def init_db():
	Base.metadata.create_all(bind=engine)
