from pydantic import BaseModel, EmailStr, Field, ConfigDict
from .constants.user_role import RoleEnum
from .constants.permissions import PermissionEnum
from .constants.tasks import TaskTagsEnum, TaskStatus
from .constants.payment import Currency, PaymentMode
from .constants.skills import SkillsEnum
from datetime import datetime

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

class UserResponse(UserBase):
    id : int

class CreateMember(UserBase):
    password : str
    permission : PermissionEnum

class TokenInfo(BaseModel):
    id : int

class Address(BaseModel):
    id : int
    uid : int
    house_number : str
    landmark : str
    area : str
    city : str
    state : str
    country : str
    pincode : str

    model_config= ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    customer_info : UserBase
    address: Address | None = None
    model_config= ConfigDict(from_attributes=True)

class CustomerResponse(CustomerBase):
    id : int
    u_id : int

class TaskerSkillBase(BaseModel):
    tasker_skill : SkillsEnum

    model_config= ConfigDict(from_attributes=True)

class TaskerSkillResponse(TaskerSkillBase):
    id : int
    tasker_id : int


class TaskerBase(BaseModel):
    skills : list[TaskerSkillResponse]
    tasks : list[TaskBase]
    model_config= ConfigDict(from_attributes=True)

class TaskerResponse(TaskerBase):
    id : int
    u_id : int
    rating : float | None = 0.0
    task_completed : int
    is_delete : bool | None = False
    is_active : bool | None = False
    created_at : datetime

class TaskBase(BaseModel):
    task_title : str
    task_description : str
    task_tag : TaskTagsEnum
    currency: Currency
    amount : int
    payment_method : PaymentMode

    model_config= ConfigDict(from_attributes=True)

class CreateTask(TaskBase):
    tasker_id : int
    pass

class TaskResponse(CreateTask):
    tasker : TaskerResponse
    task_id : int
    customer_id : int
    task_start_date : datetime | None = None
    task_end_date : datetime | None = None
    created_at : datetime
    task_status : TaskStatus | None = TaskStatus.POSTED
    # customer : 