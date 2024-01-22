from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

import time


SECRET_KEY = "too_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def signJWT(username: str) -> str:
    payload = {
        "username": username,
        "expires": time.time() + 60 * ACCESS_TOKEN_EXPIRE_MINUTES
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

credentials_exception_factory = lambda text: HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=text,
                    headers={"WWW-Authenticate": "Bearer"},
                )


class AuthController:
    def __init__(self, dam) -> None:
        self.dam = dam

    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            if not token:
                raise credentials_exception_factory("Empty token")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            expires = payload.get("expires")
            if time.time() > expires:
                raise credentials_exception_factory("Expired, you need to sign in")
            print(username)
            if username is None:
                raise credentials_exception_factory("No such user")
        except JWTError:
            raise credentials_exception_factory("Could not validate credentials")
        return username
    
    def sign(self, username, password, balance=None):
        exists = self.dam.check_user(username)
        if exists:
            token = self.sign_in(username, password)
        else:
            token = self.sign_up(username, password, balance)
        return token

    def sign_in(self, username, password):
        db_password = self.dam.get_password(username)
        if verify_password(password, db_password):
            return signJWT(username)
        raise credentials_exception_factory("Incorrect password")
    
    def sign_up(self, username, password, balance):
        pswd_hash = get_password_hash(password)
        self.dam.add_user(username, pswd_hash, balance)
        return signJWT(username)
