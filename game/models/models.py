"""Название плохо описывает суть того, что тут происходит"""
from enum import Enum


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


class CellStatus(Enum):
    DISABLE = -1
    ENABLE = 1
    FINISH = 0


class Coordinates:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Cell:

    def __init__(self, x=0, y=0,
                 cell_status: CellStatus = CellStatus.DISABLE,
                 is_box_inside=None):
        """Возможно следует убрать отсюда координаты, так как они и так уже автоматически учтены в Field"""
        self.coordinates = Coordinates(x, y)
        self.box = is_box_inside
        self.cell_status = cell_status

    @property
    def x(self):
        return self.coordinates.x

    @property
    def y(self):
        return self.coordinates.y

class Box:
    # Todo 

