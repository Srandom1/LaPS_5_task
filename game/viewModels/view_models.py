from enum import Enum

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect

from game.viewModels.abstract_view import *
from game.models import models
from game.utils import *

REDACTED_IMAGE_PATH = IMAGES_PATH + "/"


class CellIcons(Enum):
    """Каждое значение - словарь иконок (именно словарь, так как возможно придется делать анимации)"""
    player = QPixmap(REDACTED_IMAGE_PATH + "player.png")
    wall = QPixmap(REDACTED_IMAGE_PATH + "wall.png")
    floor = QPixmap(REDACTED_IMAGE_PATH + "floor.png")
    finish_mark = QPixmap(REDACTED_IMAGE_PATH + "finish_mark.png")


class CellView(CustomView):

    def __init__(self):
        super().__init__()


class BoxView(CustomView):

    def __init__(self):
        super().__init__()


class PlayerView(CustomView):

    def __init__(self):
        super().__init__()


class FinishMarkView:

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    print(IMAGES_PATH)
