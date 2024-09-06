from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# No need to import Base, List, ListItem inside the same file
Base = declarative_base()

class List(Base):
    __tablename__ = 'lists'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = relationship("ListItem", back_populates="list")

    __table_args__ = (
        Index('idx_list_type', 'type'),
        Index('idx_list_is_deleted', 'is_deleted'),  # Index to speed up queries filtering by is_deleted
    )


class ListItem(Base):
    __tablename__ = 'list_items'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('lists.id'), nullable=False)
    value = Column(String(255), nullable=False, index=True)
    comment = Column(Text)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(String(255))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    list = relationship("List", back_populates="items")

    __table_args__ = (
        Index('idx_list_value', 'value', 'list_id'),
        Index('idx_listitem_is_deleted', 'is_deleted', 'list_id'),  # Index to speed up filtering on is_deleted and list_id
    )