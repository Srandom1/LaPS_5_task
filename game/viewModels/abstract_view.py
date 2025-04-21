from abc import ABC, abstractmethod
from game.models.models import *

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

class CustomView(QWidget):

    def __init__(self):
        super().__init__()
        self.childes = []
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        self.icon = None

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._perform_animation)
        self.y_delta = 0
        self.x_delta = 0

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
        self.x_delta = 0
        self.y_delta = 0


        self.animation_timer.start()

    def _perform_animation(self):
        if self._icon_x_offset < self.target_offset_x:
            self._icon_x_offset += self.animation_step
            self.update()
        else:
            self.animation_timer.stop()