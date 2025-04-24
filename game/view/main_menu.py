import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QListWidget, QWidget, QFrame, \
    QMainWindow, QApplication

from game import parser
from game.controllers.game_controller import GameController
from game.controllers.player_controller import PlayerController
from game.models.player import Player
from game.utils import LEVELS_PATH, read_file_as_string
from game.view.game_view import GameWindow
from game.viewModels.view_models import Icons


class GameMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_levels()
        self.game_screen = None

    def initUI(self):
        # Основные параметры окна
        self.setWindowTitle("Яндекс доставка - пролог")
        self.setMinimumSize(600, 500)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный лейаут
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # Заголовок игры
        title_label = QLabel("Симулятор доставщика")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)

        # Подзаголовок
        subtitle_label = QLabel("Выберите уровень и нажмите 'Играть'")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont("Arial", 12)
        subtitle_label.setFont(subtitle_font)

        # Добавляем заголовок и подзаголовок
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addSpacing(10)

        # Создаем список уровней
        levels_label = QLabel("Доступные уровни:")
        levels_label.setFont(QFont("Arial", 12, QFont.Bold))
        main_layout.addWidget(levels_label)

        # Список уровней
        self.levels_list = QListWidget()
        self.levels_list.setMinimumHeight(200)
        main_layout.addWidget(self.levels_list)

        # Кнопка "Играть"
        self.play_button = QPushButton("ИГРАТЬ")
        self.play_button.setMinimumHeight(50)
        self.play_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.play_button.setEnabled(False)  # Изначально кнопка неактивна
        main_layout.addWidget(self.play_button)

        self.levels_list.itemClicked.connect(self.on_level_selected)
        self.play_button.clicked.connect(self.start_game)

    def load_levels(self):
        # Здесь можно загрузить уровни из файла или базы данных
        # Для примера создадим несколько уровней
        self.levels = os.listdir(LEVELS_PATH)
        # Добавляем уровни в список
        for level in self.levels:
            self.levels_list.addItem(level)

    def on_level_selected(self, item):
        index = self.levels_list.row(item)
        self.level = self.levels[index]

        self.play_button.setEnabled(True)

        self.selected_level_index = index

    def start_game(self):

        source = read_file_as_string(LEVELS_PATH + "/" + self.level)
        field = parser.generate_field_from_string(source)
        player = Player(None)
        game_controller = GameController(field, player)
        player_controller = PlayerController(player, game_controller)
        self.game_screen = GameWindow(self, field, player_controller, game_controller)
        self.game_screen.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Icons.set_icons()


    main_window = GameMenu()
    main_window.show()
    sys.exit(app.exec_())