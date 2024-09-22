import random

from math import sqrt
from abc import ABC, abstractmethod
from itertools import product
from typing import List, Tuple, Union
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

    def collide(self, circle: "Circle"):
        circle_rect = Rect(Point(circle.pos.x - circle.radius,
                                 circle.pos.y - circle.radius),
                           width=circle.radius * 2,
                           height=circle.radius * 2)
        return self.corner.x < circle_rect.corner.x + circle_rect.width and \
            self.corner.x + self.width > circle_rect.corner.x and \
            self.corner.y < circle_rect.corner.y + circle_rect.height and \
            self.corner.y + self.height > circle_rect.corner.y


@dataclass
class Circle(AbstractContainsMixin):
    pos: Point
    is_target: bool
    speed: int
    speed_vector: Point
    radius: int = 10

    def contains(self, point: Point) -> bool:
        cx, cy = self.pos.to_tuple()
        x, y = point.to_tuple()
        dist = ((cx - x) ** 2 + (cy - y) ** 2) ** (1 / 2)
        return dist <= self.radius


class Map:
    OBJECTS_COUNT = 15
    OBJECT_MAX_SPEED = 10
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
            speed = random.randint(1, self.OBJECT_MAX_SPEED)
            x_speed = random.choice((True, False))
            coeff = random.choice((1, -1))
            speed_vector = Point(x=int(x_speed) * coeff, y=int(not x_speed) * coeff)
            objects.append(Circle(Point(*pos), i == 0, speed_vector=speed_vector, speed=speed))
        return objects

    def _validate_objects(self, objects: List[Circle]):
        for rect in self._borders:
            if any(rect.contains(obj.pos) for obj in objects):
                raise MapException("Obj in border")

    def collide_with_borders(self, obj: Union[Point, Circle]) -> bool:
        if isinstance(obj, Point):
            return any(border.contains(obj) for border in self._borders)
        else:
            return any(border.collide(obj) for border in self._borders)

    def collide_with_target(self, pos: Point) -> bool:
        return self._target.contains(pos)

    def process(self):
        for obj in self._targets:
            for i in range(obj.speed):
                speed_x, speed_y = map(lambda vec: vec, obj.speed_vector.to_tuple())
                x, y = obj.pos.to_tuple()
                obj.pos = Point(x + speed_x, y + speed_y)
                if self.collide_with_borders(obj):
                    speed_vec = Point(x=int(not bool(obj.speed_vector.x)),
                                      y=int(not bool(obj.speed_vector.y)))
                    coeff_list = [1, -1]
                    random.shuffle(coeff_list)
                    for coeff in coeff_list:
                        speed_vec = Point(*map(lambda vec: vec * coeff, speed_vec.to_tuple()))
                        speed_x, speed_y = speed_vec.to_tuple()
                        obj.pos = Point(x + speed_x, y + speed_y)
                        if not self.collide_with_borders(obj):
                            obj.speed_vector = speed_vec

                speed_x, speed_y = map(lambda vec: vec, obj.speed_vector.to_tuple())
                obj.pos = Point(x + speed_x, y + speed_y)

    @property
    def borders(self) -> List[Rect]:
        return self._borders.copy()

    @property
    def targets(self) -> List[Circle]:
        return self._targets.copy()

    @property
    def target(self) -> Circle:
        return self._target
