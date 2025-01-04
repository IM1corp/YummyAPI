import unittest

from yummyanime import YummyApi, Format

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
        anime = next((i for i in data.response if i.title == 'Как и ожидал, моя школьная романтическая жизнь не удалась'), None)
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
if __name__ == '__main__':
    unittest.main()
