from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

# 		self.attempts = 10
# 		self.connect()

# 		# self.conn = mariadb.connect(**self.config)
# 		# self.cur = self.conn.cursor()


def init_engine(uri, **kwargs):
	global engine
	engine = create_engine(uri, **kwargs)
	if not database_exists(engine.url):
		create_database(engine.url)
	return engine


def init_db():
	from models import file
	Base.metadata.create_all(bind=engine)
