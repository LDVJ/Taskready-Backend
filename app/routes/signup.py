from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, models, utilities
from ..db import get_db


router = APIRouter(
    prefix="/signup",
    tags=["Signup"]
)

@router.post("/", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
def new_user(payload: schemas.CreateUser, background_tasks : BackgroundTasks,db : Session = Depends(get_db) ):
    payload_dict = payload.model_dump(exclude_unset=True)
    simp_password = payload_dict["password"]
    hash_password= utilities.create_hash_password(simp_password)
    payload_dict["password"] = hash_password
    new_user = models.User(**payload_dict)

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)

        token = utilities.create_verification_token(new_user.email)
        background_tasks.add_task(utilities.send_verification_email, email=new_user.email, token=token, name=new_user.name)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred. Please try again later.")
    return new_user
