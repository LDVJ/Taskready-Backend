from .. import models, schemas
from ..constants.user_role import RoleEnum
from ..db import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

def  user_role(data : schemas.UserResponse, db : Session = Depends(get_db)):
    if data.role == RoleEnum.CUSTOMER:
        new_customer = models.Customer(u_id = data.id)
        db.add(new_customer)
    
    elif data.role == RoleEnum.TASKER:
        new_tasker = models.Tasker(u_id = data.id)
        db.add(new_tasker)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE) 

