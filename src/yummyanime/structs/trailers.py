from ..structs import AbsDict


class ITrailerJson(AbsDict):
    def __init__(self, data: dict, **kwargs):
        if data.get('iframe_url', '').startswith('//'):
            data['iframe_url'] = 'https:' + data['iframe_url']
        if kwargs.get('iframe_url', '').startswith('//'):
            kwargs['iframe_url'] = 'https:' + kwargs['iframe_url']

    trailer_id: int
    anime_id: int
    iframe_url: str
    dubbing: str
    player: str
    number: str
