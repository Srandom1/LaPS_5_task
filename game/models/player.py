from game.models.models import *


# По хорошему сюда бахнуть валидаторы, но пишу в режиме жесткого спидрана
class Player:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance

    def __init__(self, direction:Direction):
        if not hasattr(self, 'initialized'):  # Проверяем, инициализирован ли объект
            super().__init__()
            self.camera_direction = direction
            self.position = Coordinates(0, 0)
            self.initialized = True
        if direction is not None:
            self.camera_direction = direction

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.x = value

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.y = value
