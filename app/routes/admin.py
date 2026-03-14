from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from ..db import get_db
from .. import models, schemas, utilities
from ..constants.user_role import RoleEnum
from ..auth import session


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/user", response_model= list[schemas.UserBase])
def get_admin_details(db: Session = Depends(get_db), current_user : models.User = Depends(session.get_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admin have the rights to access this")
    all_user = db.query(models.User).filter(models.User.role == RoleEnum.USER).all()

    return all_user
