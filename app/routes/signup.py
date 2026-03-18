from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from .. import schemas, models, utilities
from ..auth import session
from ..db import get_db
from ..constants.user_role import RoleEnum


router = APIRouter(
    prefix="/user",
    tags=["Signup"]
)

@router.post("/signup", response_model=schemas.UserBase, status_code=status.HTTP_201_CREATED)
def new_user(payload: schemas.CreateUser, background_tasks : BackgroundTasks,db : Session = Depends(get_db) ):
    if payload.role == RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin can't be created with this path")
    
    check_email = db.query(models.User).filter(models.User.email == payload.email).first()
    if check_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already exists")

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


@router.patch("/update", response_model=schemas.UserBase)
# @router.patch("/update")
def update_user(payload : schemas.UserBase, db : Session = Depends(get_db), current_user : models.User = Depends(session.get_user)):
    if payload.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
    payload_dict = payload.model_dump(exclude_unset=True)

    for key, items in payload_dict.items():
        setattr(current_user, key, items)
    
    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed")

    return current_user

