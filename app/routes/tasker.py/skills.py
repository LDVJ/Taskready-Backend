from fastapi import APIRouter, Depends, HTTPException, status
from ... import schemas, models
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