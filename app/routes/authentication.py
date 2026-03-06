from fastapi import APIRouter, Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..db import get_db
from .. import models,utilities
from ..auth import session
from datetime import datetime, timedelta, timezone

router = APIRouter(
    tags=["Login"]
)

@router.post("/login")
def login(response : Response, user_creds: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    check_creds = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not check_creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    verify_password = utilities.verify_hash_password(plain_password=user_creds.password,hashed_password=check_creds.password)
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    # token = utilities.create_access_token(user_data={"uid": check_creds.id,
    #                                                  "user_email":check_creds.email})
    token = session.create_access_token(user_data=check_creds.id)

    refresh_token = session.create_refresh_token(user_data=check_creds.id)

    hash_refresh = utilities.hash_refresh_token(refresh_token)

    check_refresh_table = db.query(models.UserSession).filter(models.UserSession.user_id == check_creds.id).first()
    if not check_refresh_table:
        new_refresh = models.UserSession(
            user_id = check_creds.id,
            refresh_token_hash = hash_refresh,
            expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(new_refresh)
    else:
        check_refresh_table.refresh_token_hash = hash_refresh
        check_refresh_table.expires_at = datetime.now(timezone.utc) + timedelta(days=7)    
    db.commit()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )

    return {
        "access_token" : token,
        "type" : "bearer"
        # "refresh_token": refresh_token
    }

@router.post("/refresh")
def refresh_access_token(response : Response, refresh_token : str = Cookie(None), db : Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Token Missing")
    user_info = session.verify_refresh_token(refresh_token=refresh_token)
    if user_info.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token Type")
    
    user_id = int(user_info.get("sub"))

    user_hash_token = db.query(models.UserSession).filter(models.UserSession.user_id == user_id).first()

    if not user_hash_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No Refresh Token found")

    valid_token = utilities.verify_hash_token(token=refresh_token, hash_token_db=user_hash_token.refresh_token_hash)

    if not valid_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Token not matching with the user")

    if user_hash_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Toeken Session Expired")
    
    new_access_token = session.create_access_token(user_data=user_id)
    
    new_refresh_token = session.create_refresh_token(user_data=user_id)
    new_hash = utilities.hash_refresh_token(new_refresh_token)

    user_hash_token.refresh_token_hash = new_hash
    user_hash_token.expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    db.commit()

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )

    return{
        "access_token" : new_access_token,
        "type":"bearer"
    }