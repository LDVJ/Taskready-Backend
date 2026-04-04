from fastapi import APIRouter, Depends, HTTPException, status
from ... import schemas, models
from ...constants.user_role import RoleEnum
from app.db import get_db
from sqlalchemy.orm import Session
from ...auth import session
from ...constants.user_role import RoleEnum


router = APIRouter(
    prefix="/skill",
    tags=["Skill"]
)

@router.post("/", response_model = schemas.TaskerSkillResponse)
def new_skill(payload: schemas.TaskerSkillBase, db : Session = Depends(get_db), current_user : models.User = Depends(session.get_user)):
    if not current_user.role == RoleEnum.TASKER:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This Role don't have permission")
    new_skill = models.TaskerSkill(tasker_id = current_user.id, tasker_skill = payload.tasker_skill)
    db.add(new_skill)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error from DB")

@router.get("/", response_model= list[schemas.TaskerSkillResponse])
def get_all_skill(payload: schemas.CheckTasker, db : Session = Depends(get_db), current_user : models.User = Depends(session.get_user)):
    if not (current_user.role == RoleEnum.ADMIN or current_user.role == RoleEnum.CUSTOMER):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Role don't have this permission")
    all_tasker = db.query(models.Tasker).filter(models.Tasker.u_id == payload.id).all()
    return all_tasker