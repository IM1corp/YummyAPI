import asyncio
from typing import Any, Callable

import aiohttp
import json5

from .enums import Format
from .exceptions import YummyAPIError, YummyError, YummyRateLimitError, YummyNotFoundError, YummyResponseParseFailed
from .routes import Anime
from .structs import YummyAnswer, Timing, AbsDict


class YummyApi:
    """
    The YummyApi class is used to interact with the Yummy API.
    It provides methods for making HTTP requests to the API's endpoints.
    """

    def __init__(
            self,
            x_application_token: str,
            format: Format = Format.JSON,
            api_gateway='https://api.yani.tv',
            accept: str = 'image/avif,image/webp',
            custom_headers: dict = None,
            user_token: str | None = None
    ):
        """
        Initializes a new instance of the YummyApi class.

        :param x_application_token: Public application Access token. Get from [here](https://yummyani.me/dev/applications).
        :param format: The format of the response (default is JSON).
        :param api_gateway: The base URL of the API (default is 'https://api.yani.tv').
        :param accept: The accepted response image types (default is 'image/avif,image/webp').
        :param custom_headers: Any custom headers to include in the request (default is None).
        :param user_token: The user's token (default is None).
        """
        self._format = format
        self._x_application = x_application_token
        self.api_gateway = api_gateway
        self._accept = accept
        self._custom_headers = custom_headers or {}
        self.anime = Anime(self)
        self.token = user_token

    async def method(self, path: str, method: str, data: dict | None = None, retry_count: int = 3,
                     type: Any = None) -> Any:
        """
        Makes an HTTP request to the specified path.

        :param retry_count: retry count in case of 429 error
        :param path: The path of the endpoint.
        :param method: The HTTP method to use.
        :param data: The data to send with the request (default is None).
        :return: The response from the server.
        """

        def retry(retry_count_new: int):
            return self.method(path, method, data, retry_count=retry_count_new, type=type)

        method = method.upper()
        async with aiohttp.ClientSession(headers=self._headers) as session:
            if method == 'HEAD':
                async with session.head(f'{self.api_gateway}{path}', params=data) as resp:
                    return await self._parse_response(resp, retry, retry_count)
            if method == 'GET':
                async with session.get(f'{self.api_gateway}{path}', params=data) as resp:
                    return await self._parse_response(resp, retry, retry_count, type)
            elif method == 'PUT':
                async with session.put(f'{self.api_gateway}{path}', json=data) as resp:
                    return await self._parse_response(resp, retry, retry_count, type)
            elif method == 'POST':
                async with session.post(f'{self.api_gateway}{path}', json=data) as resp:
                    return await self._parse_response(resp, retry, retry_count, type)
            elif method == 'DELETE':
                async with session.delete(f'{self.api_gateway}{path}', json=data) as resp:
                    return await self._parse_response(resp, retry, retry_count, type)
            elif method == 'PATCH':
                async with session.patch(f'{self.api_gateway}{path}', json=data) as resp:
                    return await self._parse_response(resp, retry, retry_count, type)
            else:
                raise ValueError(f'Invalid method: {method}')

    @property
    def _headers(self):
        """
        Returns the headers to be used in the HTTP request.

        :return: A dictionary containing the headers.
        """
        return {
            'X-Application': self._x_application,
            'Content-Type': 'application/json',
            'Accept': self._accept,
            'Vary': self._format.value,
            **(self._custom_headers or {}),
            **({'Authorization': f'Bearer {self.token}'} if self.token else {})
        }

    async def _parse_response(self, resp: aiohttp.ClientResponse, retry: Callable[[int], Any] = None,
                              _retry_count=3, type: Any = None) -> YummyAnswer:
        """
        Parses the response from the server.

        :param resp: The response from the server.
        :return: The parsed response.
        """
        if resp.status == 429:  # Rate limit API handler - retry 3 times
            _retry_count -= 1
            if _retry_count >= 0:
                await asyncio.sleep(5)
                return await retry(_retry_count - 1)
            raise YummyRateLimitError("Rate limit exceeded")
        if resp.method == 'HEAD':
            return YummyAnswer(resp.status == 200, self._parse_server_timing(resp.headers.get('Server-Timing', '')))
        elif resp.status == 404:
            raise YummyNotFoundError("Not found")
        try:
            if self._format == Format.XML:
                raise YummyError("Xml response is not yet supported!")
            elif self._format == Format.JSON5:
                ans = json5.loads(await resp.text())
            else:
                ans = await resp.json()
        except Exception as e:
            raise YummyResponseParseFailed(e)

        if 'error' in ans:
            error = ans['error']
            raise YummyAPIError(
                error.get('message', ''), error.get('status_code', 0), error.get('title', 'Error'),
                error.get('name', 'Undefined Error'), error.get('suberror_code', None)
            )

        timings = self._parse_server_timing(resp.headers.get('Server-Timing', ''))
        response = self._parse_type(ans.get('response'), type)
        return YummyAnswer(response, timings)

    @staticmethod
    def _parse_server_timing(server_timing_header: str) -> list[Timing]:
        """
        Parses the Server-Timing header.

        :param server_timing_header: The Server-Timing header.
        :return: A dictionary containing the parsed Server-Timing header.
        """
        answers = []
        for component in server_timing_header.split(','):
            # Split the component into its name and duration
            data = component.split(';')
            name = data[0]
            duration = next((i.replace('dur=', '') for i in data if i.startswith('dur=')), "0")
            description = next((i.replace('desc="', '').replace('"', '') for i in data if i.startswith('desc=')), "")
            answers.append(Timing(name, float(duration), description))

        return answers

    @staticmethod
    def _parse_type(ans: dict | list, type: Any):
        if not type:
            if isinstance(ans, list):
                return [YummyApi._parse_type(i, None) for i in ans]
            return AbsDict(ans)
        if isinstance(ans, list):
            if not type.__args__: raise ValueError(f"Type {type} is not a list")
            return [YummyApi._parse_type(i, type.__args__[0]) for i in ans]
        return type(ans)
