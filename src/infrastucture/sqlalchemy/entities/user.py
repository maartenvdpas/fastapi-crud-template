from typing import List, Optional
from datetime import datetime
from sqlalchemy import DateTime, String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastucture.sqlalchemy.sqlalchemy import Base

class UserEntity(Base):
    __tablename__ = "users"

    id              : Mapped[int]       = mapped_column(Integer, primary_key=True)
    email           : Mapped[str]       = mapped_column(String(320), index=True)
    password_hash   : Mapped[str]       = mapped_column(String(128), nullable=True)
    registered_at   : Mapped[datetime]  = mapped_column(DateTime)