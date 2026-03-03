from pydantic import BaseModel, EmailStr, Field, ConfigDict
from .constants.user_role import RoleEnum
from .constants.permissions import PermissionEnum

class TokenData(BaseModel):
    token : str
    type : str

class UserBase(BaseModel):
    name : str = Field(min_length=5,max_length=50)
    email : EmailStr
    mob_no : str = Field(min_length=5, max_length=10)
    profile_pic : str | None = None
    role : RoleEnum

    model_config= ConfigDict(from_attributes=True)

class CreateUser(UserBase):
    password : str

class CreateMember(UserBase):
    password : str
    permission : PermissionEnum

class TokenInfo(BaseModel):
    id : int