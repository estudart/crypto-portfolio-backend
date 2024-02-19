from marshmallow import Schema, fields

class ExecOrderSchema(Schema):
    """ Define como uma nova Ordem a ser inserido deve ser representado
    """
    symbol =  fields.Str()
    quantity = fields.Float()
    price = fields.Float()
    side = fields.Str()
    currency = fields.Str()
    data_insercao = fields.DateTime()

exec_order_schema = ExecOrderSchema()
exec_orders_schema = ExecOrderSchema(many=True)