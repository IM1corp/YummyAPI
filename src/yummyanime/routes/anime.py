from ._abs import *
from ..structs import IOneAnimeJson, YummyAnswer, ITrailerJson, AnimeRateResponse, IAnimeRateResponse, UserListResponse


class AnimeList(IApiMethods):
    async def set_it(self, anime_id: int, list: int, date: int = None):
        data = {'date': date} if date else {}
        return await self.method(f'/anime/{anime_id}/list', 'PUT', {**{'list': list}, **data})

    async def set_favorite(self, anime_id: int, date: int = None):
        return await self.method(f'/anime/{anime_id}/list/fav', 'PUT', {'date': date} if date else {})

    async def remove_favorite(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/list/fav', 'DELETE')

    async def remove_it(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/list', 'DELETE')

    async def get_users_lists(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/lists', 'GET', type=list[UserListResponse])


class AnimeRate(IApiMethods):
    async def set_rate(self, anime_id: int, rate: int):
        return await self.method(f'/anime/{anime_id}/rate', 'PUT', {'rate': rate}, type=AnimeRateResponse)

    async def remove_rate(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/rate', 'DELETE', type=AnimeRateResponse)

    async def get_anime_rates(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/rates', 'GET', type=list[IAnimeRateResponse])


class Trailers(IApiMethods):
    async def get(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/trailers', 'GET', type=list[ITrailerJson])


class Anime(IApiMethods):
    def __init__(self, api: 'YummyApi'):
        super().__init__(api)
        self.list = AnimeList(self.api)
        self.rate = AnimeRate(self.api)
        self.trailers = Trailers(self.api)

    async def get(self, id: str | int, need_videos: bool = False) -> YummyAnswer[IOneAnimeJson | None]:
        return await self.method(
            f'/anime/{id}', 'GET', {} if not need_videos else {'need_videos': 1},
            type=IOneAnimeJson
        )

    async def search(self, query: str, limit: int = 5, offset: int = 0) -> YummyAnswer[list[IOneAnimeJson]]:
        return await self.method('/search', 'GET', {'q': query, 'limit': limit, 'offset': offset},
                                 type=list[IOneAnimeJson])

    async def get_recommendations(self, anime_id: int) -> YummyAnswer[list[IOneAnimeJson]]:
        return await self.method(f'/anime/{anime_id}/recommendations', 'GET', type=list[IOneAnimeJson])

    async def do_not_recommend(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/recommend', 'DELETE', type=bool)

    async def recommend(self, anime_id: int):
        return await self.method(f'/anime/{anime_id}/recommend', 'PUT', type=bool)

    async def filter(self, filters: dict):
        return await self.method('/anime', 'GET', filters, type=list[IOneAnimeJson])
