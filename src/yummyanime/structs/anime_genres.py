from ._base import AbsDict


class IGenreJson(AbsDict):
    """Basic genre information"""
    """The title of the genre"""
    title: str
    """The ID of the genre"""
    id: int
    """The alias of the genre"""
    alias: str
    """The URL of the genre"""
    url: str

class IGenreJsonFull(IGenreJson):
    """Full genre information, including description and sub-genres"""
    """The description of the genre"""
    description: str
    """A list of sub-genres"""
    subGenres: list[IGenreJson]

class IGenreGlobal(IGenreJson):
    title: str
    href: str
    value: int
    more_titles: list[str]
    group_id: int
class IGenreGroup(AbsDict):
    title: str
    id: int
class AnimeGenresResponse(AbsDict):
    genres: list[IGenreGlobal]
    groups: list[IGenreGroup]