from ._base import AbsDict
from ._enums import AnimeStatus, IAnimeType, WorldartType
from .video import IAnimeVideo


class IPosterJson(AbsDict):
    def __init__(self, data: dict = {}, **kwargs):
        for i in data.copy():
            if data[i].startswith('//'): data[i] = 'https:' + data[i]
        for i in kwargs:
            if kwargs[i].startswith('//'): kwargs[i] = 'https:' + data[i]
        super().__init__(data, **kwargs)

    """
    Small: 33x47
    """
    small: str
    """
    Medium: 184x260px
    """
    medium: str
    """
    Big: 250x350px
    """
    big: str
    """
    Fullsize: maximum dimensions    
    """
    fullsize: str
    """
    Huge: 400x560
    """
    huge: str

    @property
    def sizes(self):
        return {
            (33, 47): self.small,
            (184, 260): self.medium,
            (250, 350): self.big,
            (400, 560): self.huge,
        }

    def for_size(self, width: int, height: int):
        for i in self.sizes:
            if i[0] >= width - 5 and i[1] >= height - 5:
                return self.sizes[i]
        return self.fullsize


class AnimeRating(AbsDict):
    counters: int
    average: float


class IAnimeRateResponse(AbsDict):
    rating: int
    count: int


class UserListResponse(AbsDict):
    list_id: int
    count: int


class AnimeRemoteIds(AbsDict):
    """
    A class to represent the remote IDs of an anime from various sources.
    """

    worldart_id: int  # The ID of the anime on World Art.
    worldart_type: WorldartType = None  # The type of the anime on World Art. It's an instance of the `WorldartType` enum.
    shikimori_id: int  # The ID of the anime on Shikimori.
    sr_id: int = None  # The ID of the anime on SovetRomantica.
    kp_id: int = None  # The ID of the anime on Kinopoisk.
    myanimelist_id: int = None  # The ID of the anime on MyAnimeList.
    anilibria_alias: str = None  # The alias of the anime on Anilibria.
    anidub_id: int = None  # The ID of the anime on AniDub.

    @property
    def worldart_url(self):
        """
        Generates the URL for the anime on World Art based on the `worldart_id` and `worldart_type`.
        If the `worldart_id` or `worldart_type` is not available, it returns `None`.
        """
        if self.worldart_id and self.worldart_type:
            return f'https://world-art.ru/{self.worldart_type}/{self.worldart_type}.php?id={self.worldart_id}'
        return None

    @property
    def shikimori_url(self):
        """
        Generates the URL for the anime on Shikimori based on the `shikimori_id`.
        If the `shikimori_id` is not available, it returns `None`.
        """
        if self.shikimori_id:
            return f'https://shikimori.one/animes/{self.shikimori_id}'
        return None

    @property
    def sr_url(self):
        """
        Generates the URL for the anime on SovetRomantica based on the `sr_id`.
        If the `sr_id` is not available, it returns `None`.
        """
        if self.sr_id:
            return f'https://sovetromantica.com/anime/{self.sr_id}'
        return None

    @property
    def anilibria_url(self):
        """
        Generates the URL for the anime on Anilibria based on the `anilibria_alias`.
        If the `anilibria_alias` is not available, it returns `None`.
        """
        if self.anilibria_alias:
            return f'https://yummyanime.anilib.top/release/{self.anilibria_alias}.html'
        return None

    @property
    def kinopoisk_url(self):
        """
        Generates the URL for the anime on Kinopoisk based on the `kp_id`.
        If the `kp_id` is not available, it returns `None`.
        """
        if self.kp_id:
            return f'https://www.kinopoisk.ru/film/{self.kp_id}'
        return None

    @property
    def myanimelist_url(self):
        """
        Generates the URL for the anime on MyAnimeList based on the `myanimelist_id`.
        If the `myanimelist_id` is not available, it returns `None`.
        """
        if self.myanimelist_id:
            return f'https://myanimelist.net/anime/{self.myanimelist_id}'
        return None


class AnimeMinAge(AbsDict):
    value: int
    title: str = None


class AnimeEpisodes(AbsDict):
    aired: int
    count: int


class IListFav(AbsDict):
    title: str
    href: str
    _class: str
    id: str
    icon: str


class UserList(AbsDict):
    is_fav: bool
    list: IListFav = None


class IUserAnimeInfo(AbsDict):
    rating: int
    list: UserList


class IAnimeStatus(AbsDict):
    value: int
    alias: AnimeStatus
    title: str
    class_: str


class IAnimeJson(AbsDict):
    anime_id: int
    anime_url: str
    poster: IPosterJson
    title: str
    description: str

    def __eq__(self, other):
        if isinstance(other, IAnimeJson):
            return other.anime_id == self.anime_id
        return False


class IOneAnimeSmallJson(IAnimeJson):
    year: int
    anime_status: IAnimeStatus
    season: int
    min_age: AnimeMinAge
    user: IUserAnimeInfo
    type: IAnimeType
    views: int
    rating: AnimeRating = None


class IAnimeVideoPreview(IAnimeJson):
    time: int
    type: IAnimeType
    year: int
    anime_status: IAnimeStatus


class ILikAble(AbsDict):
    title: str
    url: str


class IAnimeGenre(ILikAble):
    id: int
    alias: str


class IAnimeStudio(ILikAble):
    id: int


class IAnimeCreator(ILikAble):
    id: int


class IUserAnimeInfoList(IAnimeJson):
    list: IListFav


class IViewingOrderData(AbsDict):
    text: str
    id: int
    index: int


class IAnimeViewingOrder(IAnimeJson):

    data: IViewingOrderData
    anime_status: IAnimeStatus
    type: IAnimeType
    year: int
    user: IUserAnimeInfoList


class IOneAnimeJson(IOneAnimeSmallJson):
    original: str
    other_titles: list
    rating: AnimeRating
    worldart_rating: float
    shikimori_rating: float
    kp_rating: float
    myanimelist_rating: float
    anidub_rating: float
    remote_ids: AnimeRemoteIds
    creators: list[IAnimeCreator]
    studios: list[IAnimeStudio]
    videos: list[IAnimeVideo] = None
    genres: list[IAnimeGenre]
    viewing_order: list[IAnimeViewingOrder]
    translates: list
    blocked_in: list
    episodes: AnimeEpisodes


class AnimeRateResponse(AbsDict):
    rating: float
    votes: int
