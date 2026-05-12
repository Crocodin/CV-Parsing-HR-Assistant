from sqlalchemy import create_engine
from app.config.config import config


# connection to PostgreSQL
engine = create_engine(config.DATABASE_URL, echo=True)