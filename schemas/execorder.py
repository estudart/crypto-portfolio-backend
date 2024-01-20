from pydantic import BaseModel
from typing import Optional, List
from model.order import ExecOrder

class ExecOrderSchema(BaseModel):
    """ Define como uma nova Ordem a ser inserido deve ser representado
    """
    symbol: str = "BTC"
    quantity: float = 1.2
    price: float = 4200.20
    side: str = "BUY"
    currency: str = "USD"

class ExecOrderViewSchema(BaseModel):
    """ Define como uma ordem de cliente deverá ser retornado
    """
    id: int = 4
    symbol: str = "BTC"
    quantity: float = 1.2
    price: float = 4200.20
    side: str = "BUY"
    currency: str = "USD"

def show_exec_order(order: ExecOrder):
    return {
        "id": order.id,
        "symbol": order.symbol,
        "quantity": order.quantity,
        "price": order.price,
        "side": order.side,
        "currency": order.currency
    }