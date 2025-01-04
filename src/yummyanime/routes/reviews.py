from ._abs import IApiMethods
from ..structs import IReviewJsonList


class Reviews(IApiMethods):
    def get_by_user(self, user_id: int):
        return self.method(f'/users/{user_id}/reviews', 'GET', type=list[IReviewJsonList])
