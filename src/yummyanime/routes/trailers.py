from ..structs import AbsDict


class ITrailerJson(AbsDict):
    trailer_id: int
    anime_id: int
    iframe_url: str
    dubbing: str
    player: str
    number: str


