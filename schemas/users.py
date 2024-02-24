from marshmallow import Schema, fields

class UserSchema(Schema):
    """ Defines how a clietn should be returned in the api call
    """
    id = fields.Integer()
    email = fields.String()

user_schema = UserSchema()
users_schema = UserSchema(many=True)