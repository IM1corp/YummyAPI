# YummyAnime API python

This is a wrapper around [yummyanime API](https://yummyani.me/api), written in Python async.

# Installation
```bash
pip install yummyanime
#OR
pip install git+https://github.com/IM1corp/YummyAPI
```

# Getting started
Before using the API, create DEV application [here](https://yummyani.me/dev/applications).

After that, start using it right away:

```python
import asyncio
from yummyanime import YummyApi, Format

api = YummyApi("your_client_id from https://yummyani.me/dev/applications", Format.JSON)


async def main(url: str):
    anime = await api.anime.get(url, need_videos=True)
    print("Friren's anime title: ", anime.response.title)
    video_kodik = next(i for i in anime.response.videos if "kodik." in i.iframe_url)
    qualities = await video_kodik.qualities(anime.response)
    print("Link to 720p: ", qualities.p720)

asyncio.run(main('provozhayushchaya-posledniy-put-friren'))
```
