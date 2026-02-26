from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey
from datetime import datetime
from ..constants.user_role import RoleEnum
from enum import Enum


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name :  Mapped[str] = mapped_column(String(100), nullable=False)
    email : Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    mob_no : Mapped[str] = mapped_column(String(20), nullable=True)
    profile_pic : Mapped[str] = mapped_column(nullable=True)
    password : Mapped[str] = mapped_column(nullable=False)
    is_verified : Mapped[bool] = mapped_column(nullable=False, default=False)
    role : Mapped[RoleEnum] = mapped_column(Enum(RoleEnum, name = "user-role-enum"), nullable=True, )
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

class permission(Base):
    id : Mapped[int] = mapped_column(primary_key=True)
    


    uuid: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)