from sqlalchemy import create_engine
from app.config import config


# connection to PostgreSQL
engine = create_engine(config.config.DATABASE_URL, echo=True)