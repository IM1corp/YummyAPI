import asyncio
import unittest

from yummyanime import YummyApi, Format

from yummyanime.structs import UserRole

from yummyanime import YummyAPIError

api = YummyApi(
    'g3qge9dzo8sklv50',
    format=Format.JSON,
    custom_headers=None,
    user_token=None,
    api_gateway="http://test.yummy-anime.ru/api",
)


class YummyApiTEST(unittest.IsolatedAsyncioTestCase):
    async def test_get_by_id(self):
        data = await api.anime.get(1268)
        self.assertIsNotNone(data.response)
        viewing_order = data.response.viewing_order
        self.assertEqual(len(viewing_order), 6)

    async def test_search(self):
        data = await api.anime.search("Как и ожидалось, моя школьная романтическая жизнь не удалась")
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response), 1)
        anime = next(
            (i for i in data.response if i.title == 'Как и ожидал, моя школьная романтическая жизнь не удалась'), None)
        self.assertIsNotNone(anime)

    async def test_video_url(self):
        data = await api.anime.get(1268, True)
        self.assertIsNotNone(data.response)
        viewing_order = next(i for i in data.response.videos if "kodik." in i.iframe_url)
        qualities = await viewing_order.qualities(data.response)
        print("Link to p720 url:", qualities.p720)
        self.assertIn('m3u8', qualities.p720.url)

    async def test_filter_anime(self):
        animes = await api.anime.filter({'limit': 1, 'offset': 0})
        desc = animes.response[0].description
        self.assertIsNotNone(desc)

    async def test_users(self):
        data = await api.users.get(1)
        self.assertEqual(data.response.nickname, "root")

    async def test_get_genres(self):
        data = await api.anime.genres.get_by_id(21)
        self.assertEqual(data.response.title, "Охотники за головами")
        all_genres = await api.anime.genres.get_all()
        self.assertGreaterEqual(len(all_genres.response.genres), 104)

    async def test_schedule(self):
        data = await api.anime.get_schedule()
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response), 1)
        for el in data.response:
            self.assertIsNotNone(el.episodes.next_date)

    async def test_get_recommendations(self):
        data = await api.anime.get_recommendations(1268)
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response), 1)

    async def test_get_blogger_videos(self):
        data = await api.anime.get_blogger_videos(9711)
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response), 1)

    async def test_get_anime_reviews(self):
        data = await api.anime.get_anime_reviews(5022)
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response.reviews), 1)

    async def test_feed(self):
        data = await api.anime.feed()
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response.new), 1)

    async def test_user_reviews(self):
        data = await api.reviews.get_by_user(888)
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response), 1)

    async def test_check_user_exists(self):
        data = await api.users.check_exists(user_id=1)
        self.assertTrue(data.response)
        not_exists = await api.users.check_exists(user_id=999999)
        self.assertFalse(not_exists.response)

    async def test_users_filters(self):
        data = await api.users.filter(nickname="root")
        self.assertIsNotNone(data.response)
        self.assertGreaterEqual(len(data.response.items), 1)
        self.assertEqual(data.response.items[0].nickname, "root")
        datagroups = await api.users.filter(groups=[UserRole.ADMIN])
        self.assertIsNotNone(datagroups.response)
        self.assertGreaterEqual(len(datagroups.response.items), 1)
        for i in datagroups.response.items:
            self.assertIn(UserRole.ADMIN, i.roles)

    async def asyncSetUp(self):
        self.loop = asyncio.new_event_loop()

    async def asyncTearDown(self):
        self.loop.close()

    async def test_users_set_data(self):
        try:
            await api.users.set_user_data(1, nickname="root", roles=[UserRole.ADMIN])
            self.assertTrue(False)

        except YummyAPIError as e:
            self.assertEqual(e.status_code, 3)


if __name__ == '__main__':
    unittest.main()
