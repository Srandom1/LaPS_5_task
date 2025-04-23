from game.models.models import *
from game.models.player import Player

class Field:

    def __init__(self, x_size=20, y_size=20):
        self._x_size = x_size
        self._y_size = y_size
        self.player = Player
        self._cell_matrix = [[Cell(i, j) for j in range(self._x_size)] for i in range(self._y_size)]

    @property
    def x_size(self):
        return self._x_size

    @property
    def y_size(self):
        return self._y_size

    @property
    def cell_matrix(self):
        return self._cell_matrix

    def change_cell(self, x, y, cell: Cell):
        self._cell_matrix[int(y)][int(x)] = cell

    def get_cell(self, x, y):
        return self._cell_matrix[int(y)][int(x)]
