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
        Cria um cliente

        Arguments:
            nome: nome do cliente.
            telefone: telefone do cliente
            email: email do cliente
            data_insercao: data de quando o cliente foi inserido à base
        """
        self.symbol = symbol
        self.quantity = quantity
        self.price = price