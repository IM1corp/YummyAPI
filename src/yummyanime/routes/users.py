from ._abs import IApiMethods
from ..structs.user import IUser


class Users(IApiMethods):
    async def get(self, user_id: int):
        return await self.method(f'/users/id{user_id}', 'GET', type=IUser)
