from enum import Enum

from ..structs import AbsDict


class IAnimeType(AbsDict):
    value: int
    name: str
    shortname: str


class AnimeStatus(Enum):
    RELEASED = 'released'
    ONGOING = 'ongoing'
    ANNOUNCEMENT = 'announcement'
    UNKNOWN = 'Unknown'

    def __repr__(self):
        return f'AnimeStatus({self.value!r})'


class WorldartType(Enum):
    ANIMATION = 'animation'
    CINEMA = 'cinema'

    def __repr__(self):
        return f'WorldartType({self.value!r})'
