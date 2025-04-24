from abc import ABC, abstractmethod
from game.models.models import *

from PyQt5.QtCore import QRect, QRectF, Qt, QObject, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer


class AnimationManager(QObject):
    animation_completed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._active_animations = 0

    def start_animation(self):
        self._active_animations += 1

    def end_animation(self):
        self._active_animations -= 1
        if self._active_animations <= 0:
            self._active_animations = 0
            self.animation_completed.emit()

    @property
    def is_animating(self):
        return self._active_animations > 0


animation_manager = AnimationManager()


class CustomView(QGraphicsItem):
    def __init__(self):
        super().__init__()

        self.icon = None
        self.size = 0
        self.childes = []
        self.to_update_list = []
        # Анимационные параметры
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        self._animation_timer = QTimer()
        self._animation_timer.timeout.connect(self._perform_animation)
        self._y_delta = 0
        self._x_delta = 0
        self._target_offset_x = 0
        self._target_offset_y = 0
        self._modulus_increment = 3
        self._after_animate_action = None

        # Разрешаем анимацию
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setZValue(0)

    @property
    def modulus_increment(self):
        return self._modulus_increment

    @modulus_increment.setter
    def modulus_increment(self, value):
        self._modulus_increment = abs(value)

    def boundingRect(self):
        """Возвращает прямоугольник, содержащий элемент"""
        # Делаем прямоугольник немного больше, чтобы вместить анимацию
        return QRectF(-1.5 * self.size, -1.5 * self.size, self.size * 6, self.size * 6)

    def paint(self, painter, option, widget):
        """Отрисовка элемента"""
        if self.icon is None:
            return

        # Масштабируем иконку под размер ячейки
        scaled_icon = self.icon.scaled(self.size, self.size, Qt.KeepAspectRatio)

        # Рисуем с учетом смещения для анимации
        target_rect = QRectF(
            self._icon_x_offset,
            self._icon_y_offset,
            scaled_icon.width(),
            scaled_icon.height()
        )

        # Создаем исходный прямоугольник, охватывающий всю иконку
        source_rect = QRectF(0, 0, scaled_icon.width(), scaled_icon.height())

        # Отрисовка основной иконки
        painter.drawPixmap(target_rect, scaled_icon, source_rect)

    def animate(self, direction: Direction, after_animate_action=None, to_update_list=None):
        """Анимация с использованием QGraphicsItem"""
        self._x_delta = 0
        self._y_delta = 0
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        self._after_animate_action = after_animate_action
        self.to_update_list = to_update_list if to_update_list is not None else []
        if direction == Direction.UP:
            self._y_delta = -abs(self.modulus_increment)
            self._target_offset_y = -self.size
        elif direction == Direction.DOWN:
            self._y_delta = abs(self.modulus_increment)
            self._target_offset_y = self.size
        elif direction == Direction.LEFT:
            self._x_delta = -abs(self.modulus_increment)
            self._target_offset_x = -self.size
        elif direction == Direction.RIGHT:
            self._x_delta = abs(self.modulus_increment)
            self._target_offset_x = self.size
        else:
            if after_animate_action:
                after_animate_action()
            return

        # Сообщаем менеджеру анимаций о начале новой анимации
        animation_manager.start_animation()
        self._animation_timer.start(15)

    def _perform_animation(self):
        """Выполнение шага анимации"""
        needs_update = False

        if abs(self._icon_x_offset) < abs(self._target_offset_x) and self._x_delta != 0:
            self._icon_x_offset += self._x_delta
            needs_update = True
        elif abs(self._icon_y_offset) < abs(self._target_offset_y) and self._y_delta != 0:
            self._icon_y_offset += self._y_delta
            needs_update = True
        else:
            self._x_delta = 0
            self._y_delta = 0
            self._animation_timer.stop()

            # Сообщаем менеджеру анимаций о завершении анимации
            animation_manager.end_animation()

            if self._after_animate_action is not None:
                action = self._after_animate_action
                self.to_update_list = []
                self._after_animate_action = None
                action()

        if needs_update:
            self.update()
            if self.to_update_list is not None:
                for i in self.to_update_list:
                    i.update()
