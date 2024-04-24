import unittest

from yummyanime import YummyApi, Format

api = YummyApi(
    'g3qge9dzo8sklv50',
    format=Format.JSON,
    custom_headers=None,
    user_token=None,
    # api_gateway="http://test.yummy-anime.ru/api",
)


class YummyApiTEST(unittest.IsolatedAsyncioTestCase):
    async def test_base(self):
        data = await api.anime.get(1268)
        self.assertIsNotNone(data.response)
        viewing_order = data.response.viewing_order
        self.assertEqual(len(viewing_order), 6)
        print("API is working")


    async def test_video_url(self):
        data = await api.anime.get(1268, True)
        self.assertIsNotNone(data.response)
        viewing_order = next(i for i in data.response.videos if "kodik." in i.iframe_url)
        qualities = await viewing_order.qualities(data.response)
        print("Link to p720 url:", qualities.p720)
        self.assertIn('m3u8', qualities.p720.url)
        print("URL parsing is working")


if __name__ == '__main__':
    unittest.main()
