from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from typing import Union

from model import Base


class ExecOrder(Base):
    __tablename__ = 'exec_orders'

    id = Column("pk_exec_order", Integer, primary_key=True)
    symbol = Column(String(140))
    side = Column(String(5))
    quantity = Column(Float(2))
    price = Column(Float(2))
    currency = Column(String(5))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, symbol:str, side:str, quantity:float,
                 price:float, currency:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um cliente

        Arguments:
            nome: nome do cliente.
            telefone: telefone do cliente
            email: email do cliente
            data_insercao: data de quando o cliente foi inserido à base
        """
        self.symbol = symbol
        self.side = side
        self.quantity = quantity
        self.price = price
        self.currency = currency

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao