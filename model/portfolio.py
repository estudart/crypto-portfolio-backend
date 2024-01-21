from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship, Mapped
from typing import Union

from model import Base


class Portfolio(Base):
    __tablename__ = 'portfolio'

    symbol = Column(String(140), primary_key=True)
    quantity = Column(Float(2))
    price = Column(Float(2))

    def __init__(self, symbol:str, quantity:float, price:float):
        """
        Create a new Crypto inside the Portfolio

        Arguments:
            symbol: ticker of the crypto.
            quantity: total quantity amount.
            price: total spent in that crypto in cash.
            data_insercao: the data when the crypto was added to portfolio.
        """
        self.symbol = symbol
        self.quantity = quantity
        self.price = price