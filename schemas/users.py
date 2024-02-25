from marshmallow import Schema, fields

class UserSchema(Schema):
    """ Defines how a clietn should be returned in the api call
    """
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)