import jwt
from datetime import datetime, timezone, timedelta
from ..config import settings
import uuid
from fastapi import HTTPException, Depends, status
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi.security import oauth2
from ..db import get_db

OAuth2_schema = oauth2.OAuth2PasswordBearer("login")

def create_access_token(user_data: dict, expire_at : timedelta = timedelta(minutes=30), refres : bool = None):
    payload = {
        "user" : user_data,
        "exp": datetime.now(timezone.utc) + expire_at,
        "jti": str(uuid.uuid4())
    }

    access_token = jwt.encode(algorithm=settings.ALGORITHM, key=settings.SECRET_KEY, payload=payload)

    return access_token

def verify_token(bearer_token:str, error_response: HTTPException) -> str:
    try:
        payload = jwt.decode(bearer_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id =  payload.get("user")
        if user_id is None:
            raise error_response
        token_data = schemas.TokenInfo(id= user_id)
    except jwt.InvalidTokenError:
        raise error_response
    return token_data

def get_user(bearer_token : str = Depends(OAuth2_schema), db : Session = Depends(get_db)):
    error_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorised action', headers={"WWW_Authenticate":"Bearer"})
    token = verify_token(bearer_token=bearer_token,error_response=error_exception)
    # print("=============================",token)
    user_data = db.query(models.User).filter(models.User.id == token.id).first()
    return user_data

def create_refresh_token(user_data : dict):
    payload = {
        "user":user_data,
        "exp" : datetime.now(timezone.utc) + timedelta(days=7)
    }
    refresh_token = jwt.encode(payload=payload,algorithm=settings.ALGORITHM,key=settings.SECRET_KEY)

    return refresh_token

def verify_refresh_token(refresh_token : str):
    try:
        payload = jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id =  payload.get("user")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorised action', headers={"WWW_Authenticate":"Bearer"})
        token_data = schemas.TokenInfo(id= user_id)
    except jwt.InvalidTokenError as e:
        raise e
    return token_data