import random

from itertools import product
from typing import List
from dataclasses import dataclass


DIMENSION = 1000


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
class Object:
    pos: Point


class Map:
    OBJECTS_COUNT = 8
    _borders: List[Rect]
    _objects: List[Object]

    def __init__(self, borders: List[Rect], objects: List[Object] = None):
        self._borders = borders
        self._objects = objects or self._generate_objects()
        self._validate_objects(self._objects)

    def _generate_objects(self) -> List[Object]:
        objects = []
        free_positions = list(product(list(range(DIMENSION)), repeat=2))
        for obj in self._borders:
            for row_index in range(obj.corner.y, obj.corner.y + obj.height):
                for column_index in range(obj.corner.x, obj.corner.x + obj.width):
                    free_positions.remove((column_index, row_index))
        for pos in random.sample(free_positions, self.OBJECTS_COUNT):
            objects.append(Object(Point(*pos)))
        return objects

    def _validate_objects(self, objects: List[Object]):
        for rect in self._borders:
            if any(rect.contains(obj.pos) for obj in objects):
                raise MapException("Obj in border")
