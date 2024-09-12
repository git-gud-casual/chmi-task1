import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QPainter

from map import Map, JsonLoader
from map.painter import MapPainter


class MyWidget(QtWidgets.QWidget):
    _map: Map
    _painter: QPainter
    _map_painter: MapPainter

    def __init__(self):
        super().__init__()
        self._map = JsonLoader("map.json").load()
        self._painter = QPainter(self)
        self._map_painter = MapPainter(self._map, (self.width(), self.height()))

    def paintEvent(self, event):
        self._painter.begin(self)
        self._map_painter.window_size = (self.width(), self.height())
        self._map_painter.paint_objects(self._painter)
        self._painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
