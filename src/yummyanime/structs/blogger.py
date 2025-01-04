from enum import Enum
from typing import Optional

from ._base import AbsDict
from .user import UserAvatars
from .likes import ILikesJson


class IBloggerVideoCreator(AbsDict):
    avatars: UserAvatars
    nickname: str
    id: int


class IBloggerVideoDescription(AbsDict):
    small: str
    big: str


class CategoryType(Enum):
    TOP = 'top'
    REVIEW = 'review'
    AMV = 'amv'
    NEWS = 'news'
    OTHER = 'other'
    QUIZ = 'quiz'


class IBloggerVideoCategory(AbsDict):
    id: str
    title: str

    @property
    def category(self) -> CategoryType:
        return CategoryType(self.id)


class IBloggerVideoPreviews(AbsDict):
    small: str
    big: str


class IBloggerVideoAnimeJson(AbsDict):
    has_spoiler: bool
    publish_date: int
    time: Optional[int] = None
    creator: IBloggerVideoCreator
    title: str
    descriptions: IBloggerVideoDescription
    id: int
    category: IBloggerVideoCategory
    comments_count: int
    previews: IBloggerVideoPreviews
    iframe_url: str
    views: int
    likes: ILikesJson
    language: str
