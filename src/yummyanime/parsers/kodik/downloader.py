import base64
import re
from typing import Dict

import aiohttp
from bs4 import BeautifulSoup

from ..abstract_parser import AbstractParser, Quality, Qualities
from ..utils import InvalidHtmlFormatException


class KodikVideoParser(AbstractParser):
    def __init__(self, frame_url: str, session: aiohttp.ClientSession, url_from: str):
        super().__init__(frame_url, session, url_from)
        self.video_get_vars: Dict[str, str] = {}
        self.video_get_json_params: Dict[str, str] = {}
        self.json_url: str = None

    async def parse(self) -> Qualities:
        await self.load_params_from_html()
        await self.set_def_json_params()
        ans = await self.get_info_from_json()
        return ans

    async def get_info_from_json(self):
        json_data = await self.request.post(
            self.json_url, data=self.video_get_json_params,
            headers={
                'Referer': self.frame_url,
                'Origin': 'https://kodik.biz',
                'TE': 'trailers',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        )
        json_data = await json_data.json(content_type=None)
        links = json_data["links"]
        ans = Qualities()
        for key, array in links.items():
            m3u8_url = self.get_good_src(self.decode_url(array[0]["src"]), self.frame_url)
            q = Quality(m3u8_url, self.frame_url)
            ans.set(key, q)
        return ans

    async def set_def_json_params(self):
        self.video_get_json_params["bad_user"] = "false"
        self.video_get_json_params.update(self.video_get_vars)
        self.json_url = self.get_good_src(self.POST_SRC, self.frame_url)
        self.video_get_json_params['d'] = 'yummyani.me'

    async def load_params_from_html(self):
        html = await self.load_frame_from_url(self.frame_url)
        self.url_from = self.frame_url
        soup = BeautifulSoup(html, 'html.parser')
        for el in soup.find_all('script'):
            text = (el.string or '').strip()
            if text:
                m = re.findall(self.find_params_pattern, text)
                for (key, value) in m:
                    self.video_get_vars[key] = value

                m = re.search(r"videoInfo\.hash ?= ?['\"](.+?)['\"]", text)
                if m:
                    value = m.group(1)
                    self.video_get_vars["hash"] = value

        if not self.video_get_vars:
            raise InvalidHtmlFormatException("Html is invalid - no params in html")

    async def load_frame_url_from_first_frame(self):
        url = self.frame_url
        data = await self.load_frame_from_url(url)
        match = re.search(self.find_url_pattern, data)
        if not match:
            raise InvalidHtmlFormatException("Html is invalid - no src in html")
        self.url_from = self.frame_url
        self.frame_url = match.group(1)
        if self.frame_url is None:
            raise InvalidHtmlFormatException("HTML is invalid - frame url is null")
        if self.frame_url.startswith("//"):
            self.frame_url = "https:" + self.frame_url
        elif self.frame_url.startswith("/"):
            for i in url.split("/"):
                if i and i != "http:" and i != "https:":
                    self.frame_url = "https://" + i + self.frame_url
                    break

    @staticmethod
    def decode_url(src):
        try:
            ans = re.sub(
                r'[a-zA-Z]',
                KodikVideoParser.LAMBDA,
                src
            )
            data = base64.b64decode(ans)
            return data.decode('ISO-8859-1')
        except Exception:
            return src

    LAMBDA = lambda e: chr(
        (ord(e.group()) - 13) if (
                (e.group() <= 'Z' and ord(e.group()) + 13 > ord('Z')) or ord(e.group()) + 13 > ord('z'))
        else ord(e.group()) + 13
    )
    POST_SRC = "/ftor"
    find_url_pattern = re.compile(r"\.src ?= ?\\?[\"|'](.+?)\\?[\"|']")
    find_params_pattern = re.compile(r"([a-zA-Z0-9_]+?)\s?=\s?[\"|']([^'\"]+?)[\"|']")
