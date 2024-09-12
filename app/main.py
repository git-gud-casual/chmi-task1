import sys
import logging
import datetime

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPainter, QColor

from map import Map, JsonLoader
from map.painter import MapPainter

current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f'mouse_position_{current_time}.log'

logging.basicConfig(
    filename= log_filename,  # Лог будет сохраняться в файл "mouse_position.log"
    level=logging.INFO,  # Устанавливаем уровень логирования
    format='%(asctime)s - %(message)s',  # Формат сообщения с указанием времени
    datefmt='%Y-%m-%d %H:%M:%S',  # Формат времени
    encoding='UTF-8'
)


class MyWidget(QtWidgets.QWidget):
    _map: Map
    _painter: QPainter
    _map_painter: MapPainter

    def __init__(self):
        super().__init__()
        self._map = JsonLoader("map.json").load()
        self._painter = QPainter(self)
        self._map_painter = MapPainter(self._map, (self.width(), self.height()))
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.track_mouse_position)
        self.timer.start(16)  # Обновление каждые 16 мс (примерно 60 кадров в секунду)

    def paintEvent(self, event):
        self._painter.begin(self)
        self._map_painter.window_size = (self.width(), self.height())
        self._map_painter.paint_objects(self._painter)
        self._painter.end()

    def track_mouse_position(self):
        # Получаем глобальные координаты мыши
        pos = QtGui.QCursor.pos()

        # Преобразуем глобальные координаты в координаты внутри окна
        local_pos = self.mapFromGlobal(pos)
        x = local_pos.x()
        y = local_pos.y()
        # логируем положение мыши
        if (self.width() > x >= 0) and (0 <= y < self.height()):
            logging.info(f"Координаты мыши: X={x}, Y={y}")
            # Выводим координаты в консоль
            print(f"Координаты мыши: X={x}, Y={y}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
