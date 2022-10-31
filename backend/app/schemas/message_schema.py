from marshmallow import Schema, fields


class MessageSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    room_name = fields.Str()
    content = fields.Str()
