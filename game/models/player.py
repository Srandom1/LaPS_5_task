from models.models import Direction


class Player:
    def __init__(self, direction: Direction = None):
        self.direction = direction
