from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy import Enum as SQLEnum
from datetime import datetime
from ..constants.user_role import RoleEnum
from ..constants.permissions import PermissionEnum


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name :  Mapped[str] = mapped_column(String(100), nullable=False)
    email : Mapped[str] = mapped_column(String(150), nullable=False, index=True, unique=True)
    mob_no : Mapped[str] = mapped_column(String(20), nullable=True)
    profile_pic : Mapped[str] = mapped_column(nullable=True)
    password : Mapped[str] = mapped_column(nullable=False)
    is_verified : Mapped[bool] = mapped_column(nullable=False, default=False)
    role : Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum, name = "user_role_enum"), nullable=True, )
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    permission : Mapped[list["Permission"]] = relationship("Permission", back_populates="user")

class Permission(Base):
    __tablename__ = "permissions"

    id : Mapped[int] = mapped_column(primary_key=True)
    content : Mapped[PermissionEnum] = mapped_column(SQLEnum(PermissionEnum, name = "user_permission"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user : Mapped["User"] = relationship("User", back_populates="permission")
    
class UserSession(Base):
    __tablename__ = "user_sessions"

    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token_hash : Mapped[str] = mapped_column(nullable=False)
    expires_at : Mapped[datetime] = mapped_column(nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())