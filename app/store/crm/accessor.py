import typing
from typing import Optional

from app.crm.models import User

if typing.TYPE_CHECKING:
    from app.web.app import Application


class CrmAccessor:
    def __int__(self):
        self.app: Optional["Application"] = None

    async def connect(self, app: "Application"):
        self.app = app
        try:
            self.app.database['users']
        except KeyError:
            self.app.database['users'] = []

    async def disconnect(self, _: "Application"):
        self.app = None
        pass

    async def add(self, user: User):
        self.app.database['users'].append(user)

    async def list_users(self) -> list[User]:
        return self.app.database.get('users', [])

    async def get_user(self, id_) -> Optional[User]:
        for user in self.app.database['users']:
            if user.id_ == id_:
                return user
