import base64
import uuid

from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPUnauthorized,
    HTTPForbidden
)
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
    querystring_schema
)

from app.crm.models import User
from app.crm.schemes import (
    UserSchema,
    ListUserResponseSchema,
    UserGetResponseSchema,
    UserGetSchema,
    AddUserResponseSchema,
    UserIdResponseSchema
)
from app.web.app import View
from app.web.utils import json_response


class AddUserView(View):
    @docs(
        tags=('crm',),
        summary='Add new user',
        description='Add new user to dict',
    )
    @request_schema(UserSchema)
    @response_schema(AddUserResponseSchema)
    async def post(self):
        data = await self.request.json()
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add(user)
        return json_response(
            data={
                'id': str(user.id_)
            }
        )


class ListUsersView(View):
    @docs(
        tags=('crm',),
        summary='List all users',
        description='Show all users',
    )
    @response_schema(ListUserResponseSchema, 200)
    async def get(self):
        if not self.request.headers.get('Authorization'):
            raise HTTPUnauthorized
        if not check_basic_auth(
                raw_creds=self.request.headers.get('Authorization'),
                username=self.request.app.config.username,
                password=self.request.app.config.password):
            raise HTTPForbidden
        users = await self.request.app.crm_accessor.list_users()
        return json_response(
            data={
                'users': UserGetSchema().dump(users, many=True),
            }
        )


class GetUserView(View):
    @docs(
        tags=('crm',),
        summary='Get user',
        description='Get user by id',
    )
    @querystring_schema(UserIdResponseSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        id_ = self.request.query.get('id')
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(id_))
        if not user:
            raise HTTPNotFound
        return json_response(
            data={
                'user': UserGetSchema().dump(user)
            }
        )


def check_basic_auth(raw_creds: str, username: str, password: str) -> bool:
    creds = base64.b64decode(raw_creds).decode()
    parts = creds.split(':')
    if len(parts) != 2:
        return False
    return parts[0] == username and parts[1] == password
