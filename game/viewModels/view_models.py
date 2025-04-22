from enum import Enum

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect

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
    finish_mark = generate_icons_dict_template()

    @classmethod
    def set_icons(cls):
        cls.player["default"] = QPixmap(REDACTED_IMAGE_PATH + "player.png")
        cls.wall["default"] = QPixmap(REDACTED_IMAGE_PATH + "wall.png")
        cls.floor["default"] = QPixmap(REDACTED_IMAGE_PATH + "floor.png")
        cls.finish_mark["default"] = QPixmap(REDACTED_IMAGE_PATH + "finish_mark.png")


class FinishMarkView(CustomView):

    def __init__(self):
        super().__init__()


class CellView(CustomView):

    """
    Ух ну тут прикол с переопределением сигнатуры конструктора, причем добавлением обязательного аргумента, что делать
    нельзя, но я не придумал как лаконично это сделать, так что сорян. Можно, конечно, в условной метке фективно сувать
    туда None, может быть так и сделаю, но пока что так"""
    def __init__(self, cell: Cell):
        super().__init__()
        self.linked_model = cell
        if cell.cell_status != CellStatus.DISABLE:
            self.icon = Icons.floor
        else:
            self.icon = Icons.wall
        if cell.cell_status == CellStatus.FINISH:
            mark = FinishMarkView()
            # Важно в дальнейшем следить, что бы метка была последним ребенком у объекта, иначе ее просто перекроют
            self.childes.append(mark)


class BoxView(CustomView):

    def __init__(self):
        super().__init__()


class PlayerView(CustomView):

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    print(IMAGES_PATH)
