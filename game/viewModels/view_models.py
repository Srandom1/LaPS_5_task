from enum import Enum

from game.viewModels.abstract_view import *
from game.models import models
from game.utils import *


class CellIcons(Enum):
    """Каждое значение - словарь иконок (именно словарь, так как возможно придется делать анимации)"""


class CellView(CustomView):

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    print(IMAGES_PATH)

