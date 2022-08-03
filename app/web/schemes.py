from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    status = fields.Str(default='ok')
    data = fields.Dict()
