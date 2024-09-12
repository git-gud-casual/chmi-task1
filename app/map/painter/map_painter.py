from typing import Tuple

from PySide6.QtGui import QColor, QPainter, QBrush
from PySide6.QtCore import QRect, Qt, QPoint

from ..map_ import Map, Rect, DIMENSION, Circle


class MapPainter:
    _map: Map
    _window_size: Tuple[int, int]
    BORDER_COLOR = QColor("black")
    TARGET_CIRCLE_COLOR = QColor("red")
    NON_TARGET_CIRCLE_COLOR = QColor("blue")

    def __init__(self, map_: Map, window_size: Tuple[int, int]):
        self._map = map_
        self._window_size = window_size

    @property
    def window_size(self) -> Tuple[int, int]:
        return self._window_size

    @window_size.setter
    def window_size(self, window_size: Tuple[int, int]):
        self._window_size = window_size

    def paint_objects(self, painter: QPainter):
        for obj in self._map.borders:
            rect = self._rect_to_qt_rect(obj)
            painter.fillRect(rect, self.BORDER_COLOR)
        for obj in self._map.targets:
            color = self.TARGET_CIRCLE_COLOR if obj.is_target else self.NON_TARGET_CIRCLE_COLOR
            painter.setBrush(QBrush(color, Qt.BrushStyle.SolidPattern))
            painter.drawEllipse(*self._circle_to_draw_ellipse_args(obj))

    def _translate_coord(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        width, height = self._window_size
        x, y = coord
        return int(x * width / DIMENSION), int(y * height / DIMENSION)

    def _circle_to_draw_ellipse_args(self, circle: Circle) -> Tuple[QPoint, int, int]:
        point = QPoint()
        x, y = self._translate_coord(circle.pos.to_tuple())
        point.setX(x)
        point.setY(y)
        radius = int(circle.radius * self._window_size[0] / DIMENSION)
        return point, radius, radius

    def _rect_to_qt_rect(self, rect: Rect):
        x, y = self._translate_coord(rect.corner.to_tuple())
        right_x, bottom_y = self._translate_coord((rect.corner.x + rect.width, rect.corner.y + rect.height))
        rect_width, rect_height = right_x - x, bottom_y - y
        return QRect(x, y, rect_width, rect_height)
