from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models.base import BaseModel


class Combination(BaseModel):
    __tablename__ = "combinations"
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    items = Column(JSON, nullable=False) 
    category = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)  
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="combinations")
    