from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..db import get_db
from .. import models,utilities


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.get("/",)
def login(user_creds: OAuth2PasswordRequestForm, db : Session = Depends(get_db)):
    check_creds = db.query(models.User).filter(models.User.email == user_creds.username).first()
    if not check_creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    verify_password = utilities.verify_hash_password(plain_password=user_creds.password,hashed_password=check_creds.password)
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    token = utilities.create_access_token(user_data=check_creds.id)