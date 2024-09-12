import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPainter, QColor


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

        # Таймер для обновления положения мыши
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.track_mouse_position)
        self.timer.start(16)  # Обновление каждые 16 мс (примерно 60 кадров в секунду)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    def track_mouse_position(self):
        # Получаем глобальные координаты мыши
        pos = QtGui.QCursor.pos()

        # Преобразуем глобальные координаты в координаты внутри окна
        local_pos = self.mapFromGlobal(pos)

        # Выводим координаты в консоль
        print(f"Координаты мыши: X={local_pos.x()}, Y={local_pos.y()}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
