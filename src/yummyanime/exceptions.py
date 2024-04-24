class YummyError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __repr__(self):
        return f'YummyError(message="{self.message}")'


class YummyAPIError(YummyError):
    def __init__(self, message, status_code, title='Error', name='Undefined Error', suberror_code=None):
        super().__init__(message)
        self.status_code = status_code
        self.title = title
        self.name = name
        self.suberror_code = suberror_code

    def __repr__(self):
        return f'YummyAPIError(message="{self.message}", status_code={self.status_code}, title="{self.title}", name="{self.name}", suberror_code={self.suberror_code})'


class YummyRateLimitError(YummyAPIError):
    def __init__(self, msg: str):
        super().__init__(msg, 429, 'Rate limit exceeded', 'Rate limit exceeded')

    def __repr__(self):
        return f'YummyRateLimitError(message="{self.message}")'


class YummyNotFoundError(YummyAPIError):
    def __init__(self, msg: str):
        super().__init__(msg, 404, 'Not found', 'Not found')

    def __repr__(self):
        return f'YummyNotFoundError(message="{self.message}")'


class YummyResponseParseFailed(YummyError):
    def __init__(self, exception: Exception):
        self.sub_error = exception
        super().__init__(f'Failed to parse the response: {exception}')

    def __repr__(self):
        return f'YummyResponseParseFailed(message="{self.message}", sub_error={self.sub_error!r})'
