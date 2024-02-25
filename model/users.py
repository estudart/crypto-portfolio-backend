from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from model import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    portfolio = relationship("Portfolio", back_populates="user")
    executed = relationship("ExecOrder", back_populates="user")