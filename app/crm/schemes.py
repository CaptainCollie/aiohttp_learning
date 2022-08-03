from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class UserSchema(Schema):
    email = fields.Str(required=True)


class UserGetSchema(UserSchema):
    id = fields.UUID(required=True, attribute='id_')


class UserIdResponseSchema(Schema):
    id = fields.UUID()


class AddUserResponseSchema(OkResponseSchema):
    data = fields.Nested(UserIdResponseSchema)


class ListUsersSchema(Schema):
    users = fields.Nested(UserGetSchema, many=True)


class ListUserResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUsersSchema)


class UserFieldGetResponseSchema(Schema):
    user = fields.Nested(UserGetSchema)


class UserGetResponseSchema(OkResponseSchema):
    data = fields.Nested(UserFieldGetResponseSchema)
