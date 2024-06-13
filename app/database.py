import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db() -> Generator[SessionLocal, None, None]:
    """
    Function to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_database():
    """
    Function to create the database.
    This will be called on application startup.
    """
    Base.metadata.create_all(bind=engine)
