from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config.config import config

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# connection to PostgreSQL
engine = create_engine(config.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()