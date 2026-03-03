from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..db import get_db
from .. import models,utilities
from ..auth import session


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/")
def login(user_creds: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    check_creds = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not check_creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    verify_password = utilities.verify_hash_password(plain_password=user_creds.password,hashed_password=check_creds.password)
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    # token = utilities.create_access_token(user_data={"uid": check_creds.id,
    #                                                  "user_email":check_creds.email})
    token = session.create_access_token(user_data=check_creds.id)
    
    return {
        "access_token" : token,
        "type" : "bearer"
    }