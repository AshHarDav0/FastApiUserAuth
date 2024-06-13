from loguru import logger
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.pwd_security import verify_password, get_password_hash
from app.models import User
from app.token_security import create_access_token, decode_token
from app.schemas import UserBase

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


@router.post("/register", response_model=dict)
def register(user: UserBase, db: Session = Depends(get_db)):
    db_user = User.get_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User.create(db=db, username=user.username, pwd_to_be_hashed=hashed_password)

    return {"message": "User registered successfully"}


@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = User.get_by_username(db=db, username=form_data.username)
    logger.debug(f"db_user: {db_user}")
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(db_user.username, db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    logger.debug(f"Token in auth current usr: {token}")
    username = decode_token(token)
    logger.debug(f"Username in auth current usr: {username}")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User.get_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username}


@router.delete("/users/me")
def delete_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User.get_by_username(db=db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    User.delete(db=db, username=username)
    return {"message": "User deleted successfully"}
