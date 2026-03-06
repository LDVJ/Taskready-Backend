import jwt
from datetime import datetime, timezone, timedelta
from ..config import settings
import uuid
from fastapi import HTTPException, Depends, status
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi.security import oauth2
from ..db import get_db

OAuth2_schema = oauth2.OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(user_data: dict, expire_at : timedelta = timedelta(minutes=30)):
    payload = {
        "sub" : str(user_data),
        "exp": int((datetime.now(timezone.utc) + expire_at).timestamp()),
        "jti": str(uuid.uuid4()),
        "type" : "access"
    }

    access_token = jwt.encode(algorithm=settings.ALGORITHM, key=settings.SECRET_KEY, payload=payload)

    return access_token

def verify_access_token(bearer_token:str, error_response: HTTPException) -> str:
    try:
        payload = jwt.decode(bearer_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id =  payload.get("sub")
        if user_id is None:
            raise error_response
        token_data = schemas.TokenInfo(id= user_id)
    except jwt.InvalidTokenError:
        raise error_response
    return token_data

def get_user(bearer_token : str = Depends(OAuth2_schema), db : Session = Depends(get_db)):
    error_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorised action', headers={"WWW_Authenticate":"Bearer"})
    token = verify_access_token(bearer_token=bearer_token,error_response=error_exception)
    # print("=============================",token)
    user_data = db.query(models.User).filter(models.User.id == token.id).first()
    return user_data

def create_refresh_token(user_data : dict):
    payload = {
        "sub" : str(user_data),
        "exp" : int((datetime.now(timezone.utc) + timedelta(days=7)).timestamp()),
        "jti" : str(uuid.uuid4()),
        "type": "refresh"
    }
    refresh_token = jwt.encode(payload=payload,algorithm=settings.ALGORITHM,key=settings.SECRET_KEY)

    return refresh_token

def verify_refresh_token(refresh_token : str):
    try:
        payload = jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorised action', headers={"WWW_Authenticate":"Bearer"})
    except jwt.ExpiredSignatureError as e1:
        print("E1 error = = ",e1)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    except jwt.InvalidTokenError as e2:
        print("E2 error = = ",e2)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    return payload