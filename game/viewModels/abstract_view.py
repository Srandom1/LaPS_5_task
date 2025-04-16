from abc import ABC, abstractmethod

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *


class CustomView(QWidget):

    def __init__(self):
        super().__init__()
        self.childes = []
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        self.icon = None
    
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
                (self.width() - self.icon.width()) // 2,
                (self.height() - self.icon.height()) // 2,
                self.icon.width(),
                self.icon.height()
            )
            painter.drawPixmap(target_rect, self.icon)

    def animate(self):
