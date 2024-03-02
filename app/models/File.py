from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from .Base import Base
import time
from datetime import datetime


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    type = Column(String(255))
    content = Column(LargeBinary)
    created_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    deleted_at = Column(DateTime, default=None)

    def __init__(self, name, type, content, created_at=time.strftime('%Y-%m-%d %H:%M:%S'), updated_at=time.strftime('%Y-%m-%d %H:%M:%S')):
        self.name = name
        self.type = type
        self.content = content.encode('utf-8')
        self.created_at = created_at
        self.updated_at = updated_at

    def serialize(self):

        created_at = datetime.strptime(str(self.created_at), '%Y-%m-%d %H:%M:%S')
        updated_at = datetime.strptime(str(self.updated_at), '%Y-%m-%d %H:%M:%S')
        deleted_at = datetime.strptime(str(self.deleted_at), '%Y-%m-%d %H:%M:%S') if self.deleted_at is not None else None
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'content': self.content.decode('utf-8'),
            'createdAt': created_at.strftime('%Y-%m-%d'),
            'updatedAt': updated_at.strftime('%Y-%m-%d'),
            'deletedAt': deleted_at if self.deleted_at is not None else None
        }
