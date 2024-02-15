from marshmallow import Schema, fields


class PortfolioSchema(Schema):
    """ Define como uma ordem de cliente deverá ser retornado
    """
    symbol = fields.Str()
    quantity = fields.Float()
    price = fields.Float()

portfolio_schema = PortfolioSchema()
portfolios_schema = PortfolioSchema(many=True)