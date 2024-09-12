import json
from abc import ABC, abstractmethod
from typing import Union, TextIO

from .map_ import Map, Rect, List, Point


class MapLoaderException(Exception):
    pass


class AbstractLoader(ABC):
    @abstractmethod
    def _deserialize_file(self) -> List[Rect]:
        raise NotImplementedError

    def load(self) -> Map:
        borders = self._deserialize_file()
        return Map(borders)


class JsonLoader(AbstractLoader):
    _data: dict

    def __init__(self, file: Union[str, TextIO]):
        if isinstance(file, str):
            with open(file) as f:
                self._data = json.load(f)
        else:
            self._data = json.load(file)

    def _deserialize_file(self) -> List[Rect]:
        rects = []
        try:
            for border in self._data["borders"]:
                rects.append(Rect(corner=Point(**border["point"]),
                                  width=border["width"], height=border["height"]))
        except KeyError as e:
            raise MapLoaderException(f"Incorrect map file: missing key {e}")
        return rects
