from game.models.models import *
from game.models.field import *


class GameController:

    def __init__(self, field: Field, player: Player):
        self.field = field
        self.player = player
        self.is_running = True

    def move_player(self, direction: Direction, box_available=True) -> bool:
        x = self.player.x
        y = self.player.y
        delta_vector = Coordinates(0,0)
        if direction == Direction.UP:
            delta_vector.y -= 1
        elif direction == Direction.DOWN:
            delta_vector.y += 1
        elif direction == Direction.RIGHT:
            delta_vector.x += 1
        elif direction == Direction.LEFT:
            delta_vector.x -= 1
        new_x = x + delta_vector.x
        new_y = y + delta_vector.y
        self._check_for_end()

        # Проверка возможности движения
        if not self._check_for_move_to_possibility(new_x, new_y, delta_vector=delta_vector, box_available=box_available):
            return False

        # Обновление позиции игрока
        current_cell = self.field.get_cell(x, y)
        next_cell = self.field.get_cell(new_x,new_y)
        current_cell.player = False
        next_cell.player = True
        self.player.x = new_x
        self.player.y = new_y

        # Логика для коробки
        if next_cell.box:
            box_new_x = new_x + delta_vector.x
            box_new_y = new_y + delta_vector.y
            box_cell = self.field.get_cell(box_new_x, box_new_y)
            next_cell.box = False
            box_cell.box = True

        self._check_for_end()
        return True

    def _check_for_end(self):
        cells = self.field.cell_matrix
        for row in cells:
            for cel in row:
                if not cel.box and cel.cell_status == CellStatus.FINISH:
                    return
        self.is_running = False

    def _check_for_move_to_possibility(self, x, y, delta_vector=Coordinates(0, 0), box_available=True) -> bool:
        """Передавать сюда координаты точки, на которую хотим переместиться
        :param box_available: если True, то при условии, что на клетке коробка, будет считать, что движение все равно
        возможно, в противном случае, не будет.
        :param: Нужен, что бы определить направление смещения при проверке следующего блока"""
        cell = self.field.get_cell(x, y)
        if cell.cell_status == CellStatus.DISABLE:
            return False
        if cell.box:
            if not box_available:
                return False
            x += delta_vector.x
            y += delta_vector.y
            return self._check_for_move_to_possibility(x, y, box_available=False)
        return True
