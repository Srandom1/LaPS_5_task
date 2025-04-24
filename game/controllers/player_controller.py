from game.controllers.game_controller import GameController
from game.models.models import Direction
from game.models.player import Player


class PlayerController:

    def __init__(self, player: Player, game_controller: GameController):
        self.player = player
        self.game_controller = game_controller
    # Все последующие методы возвращают, был ли сдвинут игрок
    def move_up(self) -> bool:
        return self._move(Direction.UP)

    def move_down(self) -> bool:
        return self._move(Direction.DOWN)

    def move_right(self) -> bool:
        return self._move(Direction.RIGHT)

    def move_left(self) -> bool:
        return self._move(Direction.LEFT)

    def _move(self, direction: Direction) -> bool:
        if direction == self.player.camera_direction:
            return self.game_controller.move_player(direction)
        else:
            self.player.camera_direction = direction
            return False
