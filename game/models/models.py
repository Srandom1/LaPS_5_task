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
                 box=None):
        """Возможно следует убрать отсюда координаты, так как они и так уже автоматически учтены в Field"""
        self.coordinates = Coordinates(x, y)
        self.box = box
        self.cell_status = cell_status


class Box:
    def __init__(self, cell: Cell = None):
        self.cell = cell

    @property
    def is_in_finish_cell(self):
        return self.cell.cell_status == CellStatus.FINISH
