from pydantic import BaseModel
from typing import Optional, List
from model.portfolio import Portfolio


class PortfolioViewSchema(BaseModel):
    """ Define como uma ordem de cliente deverá ser retornado
    """
    #id: int = 4
    symbol: str = "BTC"
    quantity: float = 1.2
    price: float = 4200.20

def show_portfolio(portfolio: Portfolio):
    return {
        "symbol": portfolio.symbol,
        "quantity": portfolio.quantity,
        "price": portfolio.price,
        "avg_price": format(portfolio.price / portfolio.quantity, '.2f')
    }