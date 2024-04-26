from enum import Enum

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

    def __repr__(self):
        return f'UserRole("{self.value}")'


class UserAvatars(AbsDict):
    def __init__(self, data: dict = {}, **kwargs):
        for i in data.copy():
            if data[i].startswith('//'):
                data[i] = 'https:' + data[i]
        for i in kwargs:
            if kwargs[i].startswith('//'):
                kwargs[i] = 'https:' + data[i]
        super().__init__(data, **kwargs)

    small: str
    big: str
    full: str


class ShikimoriData(AbsDict):
    nickname: str
    id: int


class UserIds(AbsDict):
    vk: int = None
    tg_nickname: str = None
    shikimori: ShikimoriData = None


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
