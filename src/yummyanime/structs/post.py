from typing import Optional

from ._base import AbsDict
from .user import IUserJsonNicknameAndAva


class IPostCategory(AbsDict):
    title: str
    id: int
    uri: str
class IPostJsonSmall(AbsDict):
    id: int
    title: str
    category: IPostCategory
    created_at: int
    user: IUserJsonNicknameAndAva
    content_preview: str
    preview_image: Optional[str] = None