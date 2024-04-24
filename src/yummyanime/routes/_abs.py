import typing

from ..structs import YummyAnswer

if typing.TYPE_CHECKING:
    from ..api import YummyApi

T = typing.TypeVar('T')


class IApiMethods:
    def __init__(self, api: 'YummyApi'):
        self.api = api

    async def method(self, path: str, method: str, data: dict | None = None, type: typing.Type[T] = None) -> YummyAnswer[T]:
        return await self.api.method(path, method, data, type=type)
