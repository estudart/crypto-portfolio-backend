from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
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