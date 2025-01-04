from typing import Union

from ._base import AbsDict
from .anime import IAnimeJson, AnimeEpisodes, AnimeRating
from .post import IPostJsonSmall
from .user import IUserJsonNicknameAndAva
from .blogger import IBloggerVideoAnimeJson, IBloggerVideoCategory
class PostsResponseFeed(AbsDict):
    items: list[IPostJsonSmall]
    types: list[dict[str, Union[str, int]]]
class JsonAnimeTopCarousel(IAnimeJson):
    rating: AnimeRating
class TopCarousel(AbsDict):
    season: int
    year: int
    items: list[JsonAnimeTopCarousel]
class IScheduleAnimeJson(IAnimeJson):
    episodes: AnimeEpisodes
class BloggerPeople(AbsDict):
    count: int
    items: list[IUserJsonNicknameAndAva]
class BloggerVideos(AbsDict):
    items: list[IBloggerVideoAnimeJson]
    categories: list[IBloggerVideoCategory]
class BloggerResponseFeed(AbsDict):
    people: BloggerPeople
    videos: BloggerVideos
class IFeedVideoJson(IAnimeJson):
    date: int
    ep_title: str
    player_title: str
    dub_title: str
    video_id: int
class ILastWatchJson(IAnimeJson):
    date: int
    end_time: int
    ep_title: str
    video_id: int

class AnimeFeedResponse(AbsDict):
    announcements: list[IAnimeJson]
    recommends: list[IAnimeJson]
    new_videos: list[IFeedVideoJson]
    top_carousel: TopCarousel
    new: list[IAnimeJson]
    last_watches: list[ILastWatchJson]
    schedule: list[IScheduleAnimeJson]
    posts: PostsResponseFeed
    blogger: BloggerResponseFeed

