from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import sqlalchemy as sa
from typing import List

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = mapped_column(String(50), primary_key=True)
    balance = mapped_column(Integer)
    tasks: Mapped[List["Task"]] = relationship()
    password = mapped_column(String(50))


class Task(Base):
    __tablename__ = 'tasks'
    job_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(ForeignKey("users.username"))
    model: Mapped[str] = mapped_column(ForeignKey("models.name"))
    status: Mapped[str] = mapped_column()
    result: Mapped[str] = mapped_column(nullable=True)
    seqn: Mapped[float] = mapped_column()
    riagendr: Mapped[float] = mapped_column()
    paq605: Mapped[float] = mapped_column()
    bmxbmi: Mapped[float] = mapped_column()
    lbxglu: Mapped[float] = mapped_column()
    diq010: Mapped[float] = mapped_column()
    lbxglt: Mapped[float] = mapped_column()
    lbxin: Mapped[float] = mapped_column()

class Model(Base):
    __tablename__ = 'models'
    name: Mapped[str] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    tasks: Mapped[List["Task"]] = relationship()
