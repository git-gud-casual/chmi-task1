import random

from itertools import product
from typing import List, Tuple
from dataclasses import dataclass


DIMENSION = 1000


class MapException(Exception):
    pass


@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


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
class Circle:
    pos: Point
    is_target: bool
    radius: int = 10


class Map:
    OBJECTS_COUNT = 15
    _borders: List[Rect]
    _targets: List[Circle]

    def __init__(self, borders: List[Rect], targets: List[Circle] = None):
        self._borders = borders
        self._targets = targets or self._generate_targets()
        self._validate_objects(self._targets)

    def _generate_targets(self) -> List[Circle]:
        objects = []
        free_positions = set(product(list(range(DIMENSION)), repeat=2))
        borders_positions = set()
        for obj in self._borders:
            for row_index in range(obj.corner.y, obj.corner.y + obj.height):
                for column_index in range(obj.corner.x, obj.corner.x + obj.width):
                    borders_positions.add((column_index, row_index))

        free_positions -= borders_positions
        for i, pos in enumerate(random.sample(free_positions, self.OBJECTS_COUNT)):
            objects.append(Circle(Point(*pos), i == 0))
        return objects

    def _validate_objects(self, objects: List[Circle]):
        for rect in self._borders:
            if any(rect.contains(obj.pos) for obj in objects):
                raise MapException("Obj in border")

    @property
    def borders(self) -> List[Rect]:
        return self._borders.copy()

    @property
    def targets(self) -> List[Circle]:
        return self._targets.copy()
