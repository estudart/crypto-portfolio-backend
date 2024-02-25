from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from model import Base


class ExecOrder(Base):
    __tablename__ = 'exec_orders'
    
    id = Column("pk_exec_order", Integer, primary_key=True)
    symbol = Column(String)
    side = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    currency = Column(String)
    data_insercao = Column(DateTime, default=datetime.now())

    # Define a new column to store the user ID
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define a relationship with the User class
    user = relationship("Users", back_populates="portfolio")