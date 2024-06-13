from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    @classmethod
    def get_by_username(cls, db: Session, username: str) -> "User":
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def create(cls, db: Session, username: str, pwd_to_be_hashed: str) -> "User":
        db_user = cls(username=username, hashed_password=pwd_to_be_hashed)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def get_users(cls, db: Session, limit: int = 100):
        return db.query(cls).limit(limit).all()

    @classmethod
    def delete(cls, db: Session, username: str) -> None:
        user = db.query(cls).filter(cls.username == username).first()
        if user:
            db.delete(user)
            db.commit()
