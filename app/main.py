import sys
import logging
import datetime
import os

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QPoint
from PySide6.QtGui import QPainter

from map import Map, JsonLoader, Point
from map.map_ import DIMENSION
from map.painter import MapPainter

LOG_DIR = "logs"

current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
log_filename = os.path.join(LOG_DIR, f'mouse_position_{current_time}.log')

logging.basicConfig(
    filename=log_filename,  # Лог будет сохраняться в файл "mouse_position.log"
    level=logging.INFO,  # Устанавливаем уровень логирования
    format='%(asctime)s - %(message)s',  # Формат сообщения с указанием времени
    datefmt='%Y-%m-%d %H:%M:%S',  # Формат времени
    encoding='UTF-8'
)


class MainWindow(QtWidgets.QWidget):
    _map: Map
    _painter: QPainter
    _map_painter: MapPainter
    _last_cursor_pos: QPoint = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("hmi")

        self._map = JsonLoader("map.json").load()
        self._painter = QPainter(self)
        self._map_painter = MapPainter(self._map, (self.width(), self.height()))

        self.setMouseTracking(True)

    @staticmethod
    def _log_mouse_position(pos: QPoint):
        x = pos.x()
        y = pos.y()
        print(f"Координаты мыши: X={x}, Y={y}")
        logging.info(f"Координаты мыши: X={x}, Y={y}")

    def _cursor_return(self, pos: QPoint):
        width, height = self.width(), self.height()
        point = Point(
            int(pos.x() * DIMENSION / width),
            int(pos.y() * DIMENSION / height)
        )
        if self._map.collide_with_borders(point) and self._last_cursor_pos:
            self.cursor().setPos(self.mapToGlobal(self._last_cursor_pos))
        elif self._map.collide_with_target(point):
            logging.info(f"Цель достигнута x={pos.x()} y={pos.y()}")
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Конец")
            dlg.setText("Цель достигнута")
            dlg.resize(250, 50)
            dlg.exec()
            qpoint = QPoint()
            qpoint.setX(0)
            qpoint.setY(0)
            self.cursor().setPos(self.mapToGlobal(qpoint))
        else:
            self._last_cursor_pos = pos

    def mouseMoveEvent(self, event):
        pos = QtGui.QCursor.pos()
        # Преобразуем глобальные координаты в координаты внутри окна
        local_pos = self.mapFromGlobal(pos)
        self._log_mouse_position(local_pos)
        self._cursor_return(local_pos)

    def resizeEvent(self, event):
        self._map_painter.window_size = (self.width(), self.height())

    def paintEvent(self, event):
        self._painter.begin(self)
        self._map_painter.paint_objects(self._painter)
        self._painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
