from abc import ABC
from urllib.parse import urlparse, urljoin

import aiohttp


class Quality:
    def __init__(self, url: str, ref: str) -> None:
        self.url = url
        self.ref = ref

    def __str__(self):
        return self.url


class Qualities:
    def __init__(self):
        self.p360 = self.p720 = self.p480 = self.p1080 = None

    p360: Quality | None
    p480: Quality | None
    p720: Quality | None
    p1080: Quality | None
    p240: Quality | None

    def set(self, key: str, q: Quality):
        match key:
            case '240':
                self.p240 = q
                return
            case "360":
                self.p360 = q
                return
            case "480":
                self.p480 = q
                return
            case "720":
                self.p720 = q
                return
            case "1080":
                self.p1080 = q
                return
        raise KeyError(f"Key {key} not found in qualities")

    def __str__(self):
        return f'Qualities (360="{self.p360}", 480="{self.p480}", 720="{self.p720}", 1080="{self.p1080}")'


class ParseAnswer:
    def __init__(self, quality: Qualities, subtitle: str) -> None:
        self.qualities = quality
        self.subtitles = subtitle


class AbstractParser(ABC):
    def __init__(self, frame_url: str, session: aiohttp.ClientSession, url_from: str):
        self.request = session
        self.frame_url = frame_url
        self.url_from = url_from

    async def parse(self) -> ParseAnswer:
        raise NotImplementedError("Abstract Parser must be implement")

    @staticmethod
    def get_good_src(src: str, parent: str):
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/"):
            parent_url = urlparse(parent)
            src = urljoin(f"{parent_url.scheme or 'https'}://{parent_url.netloc}", src)
        elif not src.startswith("http"):
            parent_url = urlparse(parent)
            final_src = f"https://{parent_url.netloc}{parent_url.path}"
            if not final_src.endswith("/"):
                final_src = final_src[:final_src.rfind("/") + 1]
            src = urljoin(final_src, src)
        return src

    async def load_frame_from_url(self, url: str, ref: str = None):
        if ref is None: ref = self.url_from
        url = self.get_good_src(url, '')
        async with self.request.get(url, headers={
            'Referer': ref,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Dest': 'iframe',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        }) as response:
            ans = await response.text('utf-8')
        return ans
