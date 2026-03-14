from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, models, utilities
from ..auth import session
from ..db import get_db


router = APIRouter(
    prefix="/user",
    tags=["Signup"]
)

@router.post("/signup", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
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


# @router.patch("/update", response_model=schemas.UserBase)
@router.patch("/update")
def update_user(payload : schemas.UserBase, db : Session = Depends(get_db), current_user : models.User = Depends(session.get_user)):
    if payload.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
    payload_dict = payload.model_dump(exclude_unset=True)

    user_info = db.query(models.User).filter(models.User.id == current_user.id).first()

    for key, items in payload_dict.items():
        setattr(user_info, key, items)
    
    db.commit()
    db.refresh(user_info)

    return user_info