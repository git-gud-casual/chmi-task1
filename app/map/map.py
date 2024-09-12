import random

from typing import List
from dataclasses import dataclass


class MapException(Exception):
    pass


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rect:
    corner: Point  # Левый верхний угол
    width: int
    height: int

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Rect's width and height must be greater than zero.")

    def contains(self, point: Point) -> bool:
        x, y = self.corner.x, self.corner.y
        return x <= point.x < x + self.width and y <= point.y <= y + self.height


@dataclass
class Objects:
    pos: Point


class Map:
    OBJECTS_COUNT = 8
    _borders: List[Rect]
    _objects: List[Objects]

    def __init__(self, borders: List[Rect], objects: List[Objects] = None):
        self._borders = borders
        self._objects = objects or self._generate_objects()
        self._validate_objects(self._objects)

    def _generate_objects(self) -> List[Objects]:
        objs = []
        for _ in range(self.OBJECTS_COUNT):
            pass
        return objs

    def _validate_objects(self, objects: List[Objects]):
        for rect in self._borders:
            if any(rect.contains(obj.pos) for obj in objects):
                raise MapException("Obj in border")
