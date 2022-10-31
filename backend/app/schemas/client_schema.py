from marshmallow import Schema, fields


class ClientSchema(Schema):
    sid = fields.Str()
    username = fields.Str()
    room_name = fields.Str()
