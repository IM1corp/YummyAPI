import warnings
from enum import Enum

from .anime import IAnimeType

from ._base import AbsDict


class UserTexsts(AbsDict):
    color: int
    left: str
    right: str


class UserRole(Enum):
    ROOT = 'root'
    EDITOR = 'editor'
    SUPEREDITOR = 'supereditor'
    VIDEOBLOGGER = 'videoblogger'
    CHATADMIN = 'chatadmin'
    REVIEWER = 'reviewer'
    ADMIN = 'admin'
    OTHER = 'other'
    NEWSROOM = 'newsroom'
    @classmethod
    def _missing_(cls, value):
        warnings.warn(f'Unknown UserRole: {value}')
        return cls.OTHER


    def __repr__(self):
        return f'UserRole("{self.value}")'


class UserAvatars(AbsDict):
    def __init__(self, data: dict = {}, **kwargs):
        for i in data.copy():
            if data[i].startswith('//'): data[i] = 'https:' + data[i]
        for i in kwargs:
            if kwargs[i].startswith('//'): kwargs[i] = 'https:' + data[i]
        super().__init__(data, **kwargs)

    small: str
    big: str
    full: str


class ShikimoriData(AbsDict):
    nickname: str
    id: int

class IUserJsonNicknameAndAva(AbsDict):
    nickname: str
    avatars: UserAvatars
    id: int
class UserIds(AbsDict):
    vk: int = None
    tg_nickname: str = None
    shikimori: ShikimoriData = None
class IAnimeTypeWithSpentTime(IAnimeType):
    spent_time: int
class IHistoryView(AbsDict):
    when: int
    ep_count: int
    duration: int
class IUserWatches(AbsDict):
    sum: list[IAnimeTypeWithSpentTime]
    history: list[IHistoryView]
class IUser(AbsDict):
    bdate: int
    id: int
    last_online: int
    register_date: int
    sex: int
    texts: UserTexsts
    about: str
    avatars: UserAvatars
    roles: list[UserRole]
    nickname: str
    banned: bool
    ids: UserIds

    watches: IUserWatches
    days_online: int

class UserSort(Enum):
    ALPHABET = 'a_z'
    ALPHABET_REVERSE = 'z_a'
    REGDATE_ASC = 'regdate_asc'
    REGDATE_DESC = 'regdate_desc'
    LASTONLINE_ASC = 'lastonline_asc'
    LASTONLINE_DESC = 'lastonline_desc'
class UsersResponse(AbsDict):
    items: list[IUser]
    limit: int
    offset: int
