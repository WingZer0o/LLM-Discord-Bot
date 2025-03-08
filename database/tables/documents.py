from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector

from database.database import Base


class Document(Base):
    __tablename__ = 'Documents'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    embedding = Column(Vector(3072))