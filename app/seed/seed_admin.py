from ..db import ssession_local
from ..models import user_model
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..constants.user_role import RoleEnum
from .. import utilities
from ..config import Seed_setting

ADMIN_EMAIL = Seed_setting.ADMIN_EMAIL
ADMIN_PWD  = Seed_setting.ADMIN_PWD


def seed_admin(db : Session):
    check_admin = db.query(user_model.User).filter(user_model.User.email == ADMIN_EMAIL).first()
    if check_admin:
        return ("Admin Already Exists")
    hash_password = utilities.create_hash_password(ADMIN_PWD)
    seed_admin_user = user_model.User(
        name = "Admin User",
        email = ADMIN_EMAIL,
        password = hash_password,
        role = RoleEnum.ADMIN
    )
    db.add(seed_admin_user)
    db.commit()

def run_seeders() -> None:
    db: Session = ssession_local()

    try:
        seed_admin(db)
    except IntegrityError:
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_seeders()
    