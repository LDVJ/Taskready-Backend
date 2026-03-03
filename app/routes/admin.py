from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from ..db import get_db
from .. import models, schemas, utilities
from ..constants.user_role import RoleEnum


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# @router.get("/")
# def get_admin_details(db: Session = Depends(get_db), user : models.User = Depends(utilities.get_user)):
#     if user.role == RoleEnum.ADMIN:
#         return re