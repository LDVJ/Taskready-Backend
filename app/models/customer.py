from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .user_model import User
from sqlalchemy import String


class Customer(Base):
    __tablename__ = "customer"

    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    u_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customer_info : Mapped["User"] = relationship("User")
    address: Mapped[list["Address"]] = relationship("Address", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "address"

    id : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    uid : Mapped[int] = mapped_column(ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)

    house_number : Mapped[str] = mapped_column(String(50), nullable=False)
    landmark : Mapped[str] = mapped_column(String(100))
    area : Mapped[str] = mapped_column(String(170), nullable=False)
    city : Mapped[str] = mapped_column(String(150), nullable=False)
    state : Mapped[str] = mapped_column(String(150), nullable=False)
    country : Mapped[str] = mapped_column(String(100), nullable=False)
    pincode : Mapped[str] = mapped_column(String(6), nullable=False)
