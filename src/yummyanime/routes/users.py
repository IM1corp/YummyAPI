from typing import Optional, Union, Iterable

from ._abs import IApiMethods
from ..structs import IUser, UserSort, UserRole, YummyAnswer, UsersResponse


class Users(IApiMethods):
    async def get(self, user_id: Optional[int] = None, nickname: Optional[str] = None) -> YummyAnswer[IUser]:
        if user_id:
            data = f'id{user_id}'
        elif nickname:
            data = f'{nickname}'
        else:
            raise ValueError('You must specify either user id or nickname')
        return await self.method(f'/users/{data}', 'GET', type=IUser)

    async def check_exists(self, user_id: Optional[int] = None, nickname: Optional[str] = None) -> YummyAnswer[bool]:
        if user_id:
            data = f'id{user_id}'
        elif nickname:
            data = f'{nickname}'
        else:
            raise ValueError('You must specify either user id or nickname')
        return await self.method(f'/users/{data}', 'HEAD', type=bool)

    async def filter(self, sort: Optional[Union[UserSort, str]] = None, limit: Optional[int] = None,
                     offset: Optional[int] = None, nickname: Optional[str] = None,
                     groups: Optional[Iterable[UserRole]] = None,
                     sex: Optional[str] = None) -> YummyAnswer[UsersResponse]:
        """
        :param sort: Sort by field
        :param limit: Limit of filter
        :param offset: Offset of filter
        :param nickname: Nickname of user
        :param groups: Groups of user
        :param sex: User sex (m, w or all)

        """
        data = {}
        if sort:
            data['sort'] = sort if isinstance(sort, str) else sort.value
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset
        if nickname:
            data['nickname'] = nickname
        if groups:
            data['groups'] = ",".join([(i.value if isinstance(i, UserRole) else i) for i in groups])
        if sex:
            data["sex"] = sex
        return await self.method('/users', 'GET', data, type=UsersResponse)

    async def set_user_data(self, user_id: int, nickname: Optional[str] = None,
                            roles: Optional[Iterable[Union[UserRole, str]]] = None,
                            ):
        data = {}
        if nickname:
            data['nickname'] = nickname
        if roles:
            data['roles'] = [(i.value if isinstance(i, UserRole) else i) for i in roles]
        return await self.method(f'/users/id{user_id}', 'PATCH', data, type=bool)
