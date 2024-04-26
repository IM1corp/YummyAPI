import typing

import aiohttp

from ..parsers import get_parser
from ..structs import AbsDict
from ..parsers.abstract_parser import Qualities

if typing.TYPE_CHECKING:
    from .anime import IAnimeJson


class VideoData(AbsDict):
    player: str
    dubbing: str


class IAnimeVideo(AbsDict):
    def __init__(self, __data: dict = {}, **kwargs):
        super().__init__(__data, **kwargs)
        self.__qualities = None

    video_id: int
    data: VideoData
    number: str
    date: int
    iframe_url: str
    index: int

    async def qualities(self, anime: 'IAnimeJson') -> Qualities:
        if not hasattr(self, '__qualities'):
            async with aiohttp.ClientSession(headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            }) as session:
                parser = get_parser(self.iframe_url, session,
                                    f'https://yummyani.me/catalog/item/{anime.anime_url}')
                self.__qualities: Qualities = await parser.parse()
        return self.__qualities
