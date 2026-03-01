from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db


router = APIRouter(
    prefix="/signup",
    tags=["Signup"]
)

@router.post("/", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
def new_user(payload: schemas.CreateUser, db : Session = Depends(get_db)):
    payload_dict = payload.model_dump(exclude_unset=True)
    new_user = models.User(**payload_dict)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred. Please try again later.")
    return new_user