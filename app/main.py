import sys
import logging
import datetime
import os
from typing import Tuple

from PySide6 import QtWidgets, QtGui, QtCore
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
    TIMER_TIME_MS = 16

    def __init__(self):
        super().__init__()
        self.setWindowTitle("hmi")
        file = QtWidgets.QFileDialog.getOpenFileName()
        self._map = JsonLoader(file[0]).load()
        self._painter = QPainter(self)
        self._map_painter = MapPainter(self._map, (self.width(), self.height()))
        self.setMouseTracking(True)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._timer_event)
        self._timer.start(self.TIMER_TIME_MS)  # Обновление каждые 16 мс (примерно 60 кадров в секунду)

    def _timer_event(self):
        self._map.process()
        qpoint = point_to_q_point(self._map.target.pos, (self.width(), self.height()))
        self._log_position(qpoint, "Координаты цели")
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        # Устанавливаем курсор в нужное положение после отображения окна
        target_pos = QPoint(20, 20)  # Задай нужные координаты внутри окна
        self.cursor().setPos(self.mapToGlobal(target_pos))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:  # Проверяем, была ли нажата клавиша Esc
            self.close()  # Закрываем окно

    @staticmethod
    def _log_position(pos: QPoint, pos_object_name: str = "Координаты мыши"):
        x = pos.x()
        y = pos.y()
        print(f"{pos_object_name}: X={x}, Y={y}")
        logging.info(f"{pos_object_name}: X={x}, Y={y}")

    def _cursor_return(self, pos: QPoint):
        window_size = (self.width(), self.height())
        current_point = q_point_to_point(pos, window_size)

        if self._last_cursor_pos:
            last_point = q_point_to_point(self._last_cursor_pos, window_size)

            # Количество шагов для проверки промежуточных точек
            steps = 20
            for i in range(1, steps + 1):
                # Линейная интерполяция между последней и текущей позицией
                interp_x = last_point.x + (current_point.x - last_point.x) * i / steps
                interp_y = last_point.y + (current_point.y - last_point.y) * i / steps
                intermediate_point = Point(int(interp_x), int(interp_y))

                if self._map.collide_with_borders(intermediate_point):
                    # Возвращаем курсор в последнее допустимое положение
                    self.cursor().setPos(self.mapToGlobal(self._last_cursor_pos))
                    return

        # Если нет столкновения, обновляем последнее положение курсора
        if self._map.collide_with_target(current_point):
            logging.info(f"Цель достигнута x={pos.x()} y={pos.y()}")
            self._timer.stop()
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Конец")
            dlg.setText("Цель достигнута")
            dlg.resize(250, 50)
            dlg.exec()
            self._timer.start()
            qpoint = QPoint(20, 20)
            self.cursor().setPos(self.mapToGlobal(qpoint))
        else:
            self._last_cursor_pos = pos

    def mouseMoveEvent(self, event):
        pos = QtGui.QCursor.pos()
        # Преобразуем глобальные координаты в координаты внутри окна
        local_pos = self.mapFromGlobal(pos)
        self._log_position(local_pos)
        self._cursor_return(local_pos)

    def resizeEvent(self, event):
        self._map_painter.window_size = (self.width(), self.height())

    def paintEvent(self, event):
        self._painter.begin(self)
        self._map_painter.paint_objects(self._painter)
        self._painter.end()


def q_point_to_point(qpoint: QPoint, window_size: Tuple[int, int]) -> Point:
    width, height = window_size
    return Point(
        int(qpoint.x() * DIMENSION / width),
        int(qpoint.y() * DIMENSION / height)
    )


def point_to_q_point(point: Point, window_size: Tuple[int, int]) -> QPoint:
    width, height = window_size
    x, y = point.to_tuple()
    x, y = int(x * width / DIMENSION), int(y * height / DIMENSION)
    qpoint = QPoint()
    qpoint.setX(x)
    qpoint.setY(y)
    return qpoint


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
