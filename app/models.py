#app/models
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db_setup import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    username: str
    password: str

class List(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String, index=True)
    is_deleted = Column(Integer, default=0)

class ListItem(Base):
    __tablename__ = "list_items"
    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    value = Column(String)
    is_deleted = Column(Integer, default=0)
    created_by = Column(String)
    comment = Column(String)
    list = relationship("List")