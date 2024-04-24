import re
import typing
import warnings


class AbsDict:
    __annotations__ = {}

    def __init__(self, __data: dict={}, **kwargs):
        data = {**__data, **kwargs}
        self._parse_annotations(data)

    @classmethod
    def get_annotations(cls):
        d = {}
        for c in cls.mro():
            try:
                d.update(**c.__annotations__)
            except AttributeError:
                # object, at least, has no __annotations__ attribute.
                pass
        return d

    def _parse_annotations(self, data: dict):
        annotations = self.get_annotations()
        for i in data:
            setattr(self, self.format_name(i), self._format(annotations, i, data[i]))

    def _format(self, annotations: dict, name: str, element: typing.Any):
        if element is None: return None
        if name in annotations:
            if isinstance(element, list) and annotations[name] is not list and annotations[name].__args__:
                annotations_new = {'z': annotations[name].__args__[0]}
                name = 'z'
                return [self._format(annotations_new, name, i) for i in element]
            return annotations[name](element)
        if isinstance(element, (str, int, float)):
            return element
        elif isinstance(element, dict):
            warnings.warn(f"Unknown type for {name} in {self.__class__.__name__}")
            return AbsDict(element)
        warnings.warn(f"Unknown type for {name} in {self.__class__.__name__}")
        return element

    @staticmethod
    def format_name(i):
        if i == 'class':
            return '_class'
        return i
    def __repr__(self):
        def format_it(value=None):
            if isinstance(value, AbsDict):
                return value.__repr__()
            if isinstance(value, list):
                if not value: return f'[]'
                return f'[{", ".join([format_it(q) for q in value])}]'
            return repr(value)

        return f'''{self.__class__.__name__}({', '.join([f'{j}={format_it(getattr(self, j))}' for j in self.__dict__])})'''

    def __str__(self, i=0):

        def format_it(i, value=None):
            tabs = ('\t' * (i + 2))
            sep = ',\n' + tabs
            if isinstance(value, AbsDict):
                return value.__str__(i + 1)
            if isinstance(value, list):
                if not value: return f'[]'
                return f'[\n{tabs}{sep.join([format_it(i + 1, q) for q in value])}\n{tabs[:-1]}]'
            return repr(value)
        tabs = ('\t' * (i + 1))
        sep = ',\n' + tabs

        return f'''{self.__class__.__name__}(
{tabs}{sep.join([f'{j}={format_it(i, getattr(self, j))}' for j in self.__dict__])}
{tabs[:-1]})'''


class Timing:
    def __init__(self, name: str, duration_ms: float, description: str = ''):
        self.name = name
        self.duration = duration_ms / 1000
        self.description = description

    def __repr__(self):
        return f'<Timing {self.name} {self.duration}s, desc="{self.description}">'


T = typing.TypeVar("T")


class YummyAnswer(typing.Generic[T]):
    def __init__(self, data: T, timings: list[Timing] = None):
        self.response = data
        self.timings = timings or []

