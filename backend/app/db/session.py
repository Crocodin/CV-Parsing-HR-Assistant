from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config.config import config

Base = declarative_base()

# connection to PostgreSQL
engine = create_engine(config.DATABASE_URL, echo=True)