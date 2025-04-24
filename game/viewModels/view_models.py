from enum import Enum

from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtCore import QRect

from game.models.player import Player
from game.viewModels.abstract_view import *
from game.models import models
from game.utils import *

REDACTED_IMAGE_PATH = IMAGES_PATH + "/"

def generate_icons_dict_template():
    return {"default": None}


class Icons:
    """Каждое значение - словарь иконок (именно словарь, так как возможно придется делать анимации основанные на замене картинок)
    такое своеобразное создание иконок в 2 этапе связано с особенностями работы с Qt"""
    player = generate_icons_dict_template()
    wall = generate_icons_dict_template()
    floor = generate_icons_dict_template()
    box = generate_icons_dict_template()
    finish_mark = generate_icons_dict_template()

    @classmethod
    def set_icons(cls):
        cls.player["default"] = QPixmap(REDACTED_IMAGE_PATH + "player.png")
        cls.wall["default"] = QPixmap(REDACTED_IMAGE_PATH + "wall.png")
        cls.floor["default"] = QPixmap(REDACTED_IMAGE_PATH + "floor.png")
        cls.finish_mark["default"] = QPixmap(REDACTED_IMAGE_PATH + "finish_mark.png")
        cls.box["default"] = QPixmap(REDACTED_IMAGE_PATH + "box.png")


class FinishMarkView(CustomView):

    def __init__(self):
        super().__init__()
        self.icon = Icons.finish_mark["default"]
        self.setZValue(4)

    def animate(self, direction, action, *args, **kwargs):
        """Так как нам не надо анимировать"""
        if action:
            action()


class CellView(CustomView):
    """
    Ух ну тут прикол с переопределением сигнатуры конструктора, причем добавлением обязательного аргумента, что делать
    нельзя, но я не придумал как лаконично это сделать, так что сорян. Можно, конечно, в условной метке фективно сувать
    туда None, может быть так и сделаю, но пока что так"""

    def __init__(self, cell: Cell = None):
        super().__init__()
        self.cell = cell
        self._pending_revalidation = False

        # Немножко костыль, что бы вписать опциональность аргумента. Но в самой игре такой ситуации поидее быть не может
        if self.cell is None:
            self.icon = Icons.wall["default"]
            return

        if self.cell.cell_status != CellStatus.DISABLE:
            self.icon = Icons.floor["default"]
        else:
            self.icon = Icons.wall["default"]

        self.revalidate()

    def revalidate(self):
        # Если анимация активна, отложим перевалидацию
        if animation_manager.is_animating:
            self._pending_revalidation = True
            animation_manager.animation_completed.connect(self._handle_animation_completed)
            return

        # Удаляем предыдущих дочерних элементов
        for child in self.childItems():
            self.scene().removeItem(child)

        # Создаем и добавляем новых дочерних элементов
        if self.cell.box:
            box = BoxView()
            box.setParentItem(self)
            box.size = self.size
            # Центрируем в родительском элементе
            box.setPos(0, 0)

        if self.cell.cell_status == CellStatus.FINISH:
            mark = FinishMarkView()
            mark.setParentItem(self)
            mark.size = self.size
            mark.setPos(0, 0)

        if self.cell.player:
            player = PlayerView(Player(None))
            player.setParentItem(self)
            player.size = self.size
            player.setPos(0, 0)
        self.update()

    def _handle_animation_completed(self):
        if self._pending_revalidation:
            self._pending_revalidation = False
            # Отсоединяем сигнал, чтобы избежать множественных вызовов
            animation_manager.animation_completed.disconnect(self._handle_animation_completed)
            self.revalidate()

    def animate(self, direction: Direction, action=None, to_update=None):
        has_children = len(self.childItems()) > 0

        if has_children:
            # Создаем обертку для действия, которое будет выполнено после всех анимаций
            def after_all_animations():
                if action:
                    action()

            # Количество анимируемых дочерних элементов
            child_count = len(self.childItems())
            animation_counter = [0]  # Используем список для возможности изменения внутри замыкания

            # Создаем обработчик завершения анимации для каждого дочернего элемента
            def child_animation_completed():
                animation_counter[0] += 1
                if animation_counter[0] >= child_count:
                    after_all_animations()

            # Запускаем анимацию для каждого дочернего элемента
            for child in self.childItems():
                child.animate(direction, child_animation_completed, to_update)
        else:
            # Если нет дочерних элементов, просто выполняем действие
            if action:
                action()


class BoxView(CustomView):

    def __init__(self):
        super().__init__()
        self.setZValue(3)
        self.icon = Icons.box["default"]


# Так как игрок только один, мы обеспечим это на прямую в коде
class PlayerView(CustomView):
    _instance = None
    _UP_ANGLE = 0
    _RIGHT_ANGLE = 90
    _DOWN_ANGLE = 180
    _LEFT_ANGLE = 270

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PlayerView, cls).__new__(cls)
        return cls._instance

    def __init__(self, player=None):
        self._icon_x_offset = 0
        self._icon_y_offset = 0
        if not hasattr(self, 'initialized'):  # Проверяем, инициализирован ли объект
            super().__init__()
            self.setZValue(100)
            self.player = player
            self.icon = Icons.player["default"]
            self.initialized = True  # Устанавливаем флаг инициализации
        if player is not None:
            self.player = player

    def get_angle_by_camera_direction(self):
        if self.player.camera_direction == Direction.UP:
            return self._UP_ANGLE
        elif self.player.camera_direction == Direction.RIGHT:
            return self._RIGHT_ANGLE
        elif self.player.camera_direction == Direction.DOWN:
            return self._DOWN_ANGLE
        elif self.player.camera_direction == Direction.LEFT:
            return self._LEFT_ANGLE
        else:
            return 0

    def paint(self, painter, option, widget):
        """Отрисовка элемента"""
        if self.icon is None:
            return

        transform = QTransform()
        transform.rotate(self.get_angle_by_camera_direction())
        # Масштабируем иконку под размер ячейки
        transformed_icon = self.icon.scaled(self.size, self.size, Qt.KeepAspectRatio).transformed(transform)

        # Рисуем с учетом смещения для анимации
        target_rect = QRectF(
            self._icon_x_offset,
            self._icon_y_offset,
            transformed_icon.width(),
            transformed_icon.height()
        )

        # Создаем исходный прямоугольник, охватывающий всю иконку
        source_rect = QRectF(0, 0, transformed_icon.width(), transformed_icon.height())

        # Отрисовка основной иконки
        painter.drawPixmap(target_rect, transformed_icon, source_rect)

if __name__ == "__main__":
    print(IMAGES_PATH)
