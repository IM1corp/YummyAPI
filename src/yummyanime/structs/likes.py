from ._base import AbsDict


class ILikesJson(AbsDict):
    likes: int
    dislikes: int
    """
    Either 0 (natural) or 1 (liked) or -1 (disliked)
    """
    vote: int
