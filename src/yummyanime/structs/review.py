from enum import Enum
from typing import Optional

from .likes import ILikesJson
from ._base import AbsDict
from .anime import IOneAnimeSmallJson
from .user import IUserJsonNicknameAndAva


class ReviewRating(AbsDict):
    average: Optional[int]
    category: Optional[dict[str, int]]


class IReviewJson(AbsDict):
    review_id: int
    update_date: int
    create_date: int

    anime_id: int
    type: str
    published_by: int
    commentable: bool
    rating: Optional[ReviewRating] = None
    check_comment: Optional[str] = None
    views: int
    author: IUserJsonNicknameAndAva
    likes: ILikesJson

    """
    @Deprecated
    """
    user_id: int
    """
    @Deprecated
    """
    total_likes: int
    """
    @Deprecated
    """
    avatar: AbsDict
    """
    @Depreacted
    """
    nickname: str
    """
    @Deprecated
    """
    user_roles: list[str]


class IReviewAnime(IReviewJson):
    text_html: str


class IReviewJsonList(IReviewJson):
    anime: IOneAnimeSmallJson
    comments_count: int


class IReviewFullJson(IReviewJsonList):
    text_html: str
    """
    Author reviews count
    """
    reviews_count: int


class ReviewsSortType(Enum):
    NEW = 'new'
    TOP = 'top'
    OLD = 'old'


class AnimeReviewsResponse(AbsDict):
    reviews: list[IReviewAnime]
    can_add: bool
