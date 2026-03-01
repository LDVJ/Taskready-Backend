from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models,utilities

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/verify")
def verify_user(token :str, db : Session = Depends(get_db)):
    user_info = utilities.verify_verification_email(token=token)
    user = db.query(models.User).filter(models.User.email == user_info["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not Found")
    if user.is_verified:
        return RedirectResponse(url="http://google.com")
    user.is_verified = True
    db.commit()
    # if user.is_verified:
    #     return RedirectResponse(url="http://google.com")


    return {
        "User_email":user.email,
        "user_name":user.name,
        "is_verified":user.is_verified
    }
    
    