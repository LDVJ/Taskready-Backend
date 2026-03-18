from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func
from ..db import Base
from .user_model import User
from .customer import Customer
from ..constants.skills import SkillsEnum
from ..constants.tasks import TaskTagsEnum, TaskStatus
from ..constants.payment import PaymentMode, Currency
from datetime import datetime
from sqlalchemy import String
from sqlalchemy import Enum as SQLENUM


class Tasker(Base):
    __tablename__ = "tasker"

    u_id : Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True,nullable=False)
    skills : Mapped[list["TaskerSkill"]] = relationship("TaskerSkill", cascade="all, delete-orphan")
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    rating : Mapped[float] = mapped_column(default=0.0, nullable=False)
    is_delete : Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active : Mapped[bool] = mapped_column(nullable=False, default=False)
    task_completed : Mapped[int] = mapped_column(default=0, nullable=False)
    tasks : Mapped[list["Tasks"]] = relationship("Tasks", back_populates="tasker")

class Tasks(Base):
    __tablename__ = "tasks"

    task_id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    tasker_id : Mapped[int] = mapped_column(ForeignKey("tasker.u_id", ondelete="CASCADE"))
    tasker : Mapped["Tasker"] = relationship("Tasker", back_populates="tasks")
    customer_id : Mapped[int] = mapped_column(ForeignKey("customer", ondelete="CASCADE"), nullable=False) 
    customer : Mapped["Customer"] = relationship("Customer")
    task_title : Mapped[str] = mapped_column(String(100), nullable=False)
    task_description : Mapped[str] = mapped_column(String)
    task_tag : Mapped[TaskTagsEnum] = mapped_column(SQLENUM(TaskTagsEnum, name = "Task_tags_enum"), nullable=False)
    currency: Mapped[Currency] = mapped_column(SQLENUM(Currency, name="currency_enum"))
    amount : Mapped[int] = mapped_column(nullable=False)
    payment_method : Mapped[PaymentMode] = mapped_column(SQLENUM(PaymentMode, name = "payment_method_enum"), nullable=False)
    task_status : Mapped[TaskStatus] = mapped_column(SQLENUM(TaskStatus, name = "Task_status_enum"), server_default=TaskStatus.POSTED)
    task_start_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    task_end_date : Mapped[datetime] =  mapped_column(DateTime(timezone=True), nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TaskerSkill(Base):
    __tablename__ = "taskerskill"

    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    tasker_id : Mapped[int] = mapped_column(ForeignKey("tasker.u_id", ondelete="CASCADE"), nullable=False)
    tasker_skill : Mapped[SkillsEnum] = mapped_column(SQLENUM(SkillsEnum, name = "skills_enum"))