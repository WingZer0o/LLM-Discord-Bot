from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.database import Base

class ChatMessage(Base):
    __tablename__ = "ChatMessages"

    Id = Column(Integer, primary_key=True)
    Message = Column(String, nullable=False),
    Author = Column(String(250), nullable=False)
    IsBot = Column(Boolean, nullable=False)
    CreatedAt = Column(DateTime)