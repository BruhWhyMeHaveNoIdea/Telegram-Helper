from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import config
from bot.tools.plugins.config import config

db_url = config['db_url']

engine = create_engine(db_url, echo=True)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)

