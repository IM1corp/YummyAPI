import aiohttp

from .kodik import KodikVideoParser


def get_parser(iframe_url: str, session: aiohttp.ClientSession, url_from: str):
    if "kodik" in iframe_url:
        return KodikVideoParser(iframe_url, session, url_from)
    raise NotImplemented(f"Parser not implemented: {iframe_url}")
