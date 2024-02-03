from sqlalchemy import Column, String, Float
from model import Base


class Portfolio(Base):
    __tablename__ = 'portfolio'

    symbol = Column(String, primary_key=True)
    quantity = Column(Float)
    price = Column(Float)