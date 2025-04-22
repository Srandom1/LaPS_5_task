from abc import ABC, abstractmethod
from game.models.models import *

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer


class CustomView(QWidget):
    # TODO При анимации персонажа подумать, как делать перепивязку текущего объекта к другому, возможно
    #  придется занулять параметры анимации, в частности текущее смещение
    def __init__(self):
        super().__init__()
        self.childes = []
        #Связаная с объектом модель
        self.linked_model = None
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        self.icon = None

        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._perform_animation)
        self._y_delta = 0
        self._x_delta = 0
        self._target_offset_x = 0
        self._target_offset_y = 0

        self._modulus_increment = 3

    @property
    def modulus_increment(self):
        return self._modulus_increment

    @modulus_increment.setter
    def modulus_increment(self, value):
        self._modulus_increment = abs(value)

    def paint_recursively(self):
        """Служит для отрисовки всех дочерних элементов, включая отрисовки самого элемента"""
        self.childes: list[CustomView]
        self.paintEvent(None)
        for child in self.childes:
            child.paintEvent(None)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.icon.isNull():
            # Рисуем иконку по центру виджета
            target_rect = QRect(
                (self.width() - self.icon.width()) // 2 + self._icon_x_offset,
                (self.height() - self.icon.height()) // 2 + self._icon_y_offset,
                self.icon.width(),
                self.icon.height()
            )
            painter.drawPixmap(target_rect, self.icon)

    def animate(self, direction: Direction):
        """Анимация в текущей ее реализации не предполагает смещение по двум осям координат сразу.
        при передачи направления устанавливается некоторый целевой отступ и шаг"""
        self._x_delta = 0
        self._y_delta = 0
        # не придумал как лучше сделать, так что терпите ifки
        if direction == Direction.UP:
            self._y_delta = -abs(self.modulus_increment)
            self._target_offset_y = -self.icon.height()
        elif direction == Direction.DOWN:
            self._y_delta = -abs(self.modulus_increment)
            self._target_offset_y = self.icon.height()
        elif direction == Direction.LEFT:
            self._x_delta = -abs(self.modulus_increment)
            self._target_offset_x = -self.icon.height()
        elif direction == Direction.RIGHT:
            self._x_delta = abs(self.modulus_increment)
            self._target_offset_x = self.icon.height()
        else:
            # Вот это на случае если нам передали какую-то хрень
            return
        self._animation_timer.start()

    def _perform_animation(self):
        """Запускает анимацию в соответствии с заданными параметрами анимации такие, как приращение по оси и целевое
         смещение"""
        # Модуль берется из-за того, что движение может быть в отрицательном направлении.
        if abs(self._icon_x_offset) < abs(self._target_offset_x) and self._x_delta != 0:
            self._icon_x_offset += self._x_delta
        elif abs(self._icon_y_offset) < abs(self._target_offset_y) and self._y_delta != 0:
            self._icon_y_offset += self._icon_y_offset
        else:
            # Во избежания неожиданного поведения при запуске новой анимации для объекта.
            self._x_delta = 0
            self._y_delta = 0
            self._animation_timer.stop()
        self.update()
