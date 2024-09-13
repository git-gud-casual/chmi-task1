import random

from abc import ABC, abstractmethod
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


class AbstractContainsMixin(ABC):
    @abstractmethod
    def contains(self, point: Point) -> bool:
        raise NotImplementedError


@dataclass
class Rect(AbstractContainsMixin):
    corner: Point  # Левый верхний угол
    width: int
    height: int

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Rect's width and height must be greater than zero.")

    def contains(self, point: Point) -> bool:
        x, y = self.corner.to_tuple()
        return x <= point.x < x + self.width and y <= point.y < y + self.height


@dataclass
class Circle(AbstractContainsMixin):
    pos: Point
    is_target: bool
    speed: Point
    radius: int = 10

    def contains(self, point: Point) -> bool:
        cx, cy = self.pos.to_tuple()
        x, y = point.to_tuple()
        dist = ((cx - x) ** 2 + (cy - y) ** 2) ** (1 / 2)
        return dist <= self.radius


class Map:
    OBJECTS_COUNT = 15
    OBJECT_X_MAX_SPEED = 10
    OBJECT_Y_MAX_SPEED = 10
    _borders: List[Rect]
    _targets: List[Circle]
    _target: Circle

    def __init__(self, borders: List[Rect], targets: List[Circle] = None):
        self._borders = borders
        self._targets = targets or self._generate_targets()
        try:
            self._target = list(filter(lambda x: x.is_target, self._targets))[0]
        except IndexError:
            raise MapException("Target does not exist")
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
            speed = Point(random.randint(1, self.OBJECT_X_MAX_SPEED) * random.choice((-1, 1)),
                          random.randint(1, self.OBJECT_Y_MAX_SPEED) * random.choice((-1, 1)))
            objects.append(Circle(Point(*pos), i == 0, speed))
        return objects

    def _validate_objects(self, objects: List[Circle]):
        for rect in self._borders:
            if any(rect.contains(obj.pos) for obj in objects):
                raise MapException("Obj in border")

    def collide_with_borders(self, pos: Point) -> bool:
        return any(border.contains(pos) for border in self._borders)

    def collide_with_target(self, pos: Point) -> bool:
        return self._target.contains(pos)

    def process(self):
        for obj in self._targets:
            speed_x, speed_y = obj.speed.to_tuple()
            x, y = obj.pos.to_tuple()
            for v in ((1, 0), (0, 1), (1, 1)):
                new_point = Point(x + speed_x * v[0], y + speed_y * v[1])
                if (not all(0 <= coord < DIMENSION for coord in new_point.to_tuple()) or
                        self.collide_with_borders(new_point)):
                    multipliers = tuple(-1 if coord else 1 for coord in v)
                    speed = Point(speed_x * multipliers[0], speed_y * multipliers[1])
                    obj.speed = speed
                    break

            obj.pos = Point(x + obj.speed.x, y + obj.speed.y)

    @property
    def borders(self) -> List[Rect]:
        return self._borders.copy()

    @property
    def targets(self) -> List[Circle]:
        return self._targets.copy()

    @property
    def target(self) -> Circle:
        return self._target
