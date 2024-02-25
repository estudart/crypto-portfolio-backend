from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from model import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column('pk_users' , Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

    portfolios = relationship("Portfolio", back_populates="users")