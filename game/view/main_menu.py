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
        self.setWindowTitle("Моя Игра - Главное меню")
        self.setMinimumSize(600, 500)

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный лейаут
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # Заголовок игры
        title_label = QLabel("НАЗВАНИЕ ИГРЫ")
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

        # Информация о выбранном уровне
        self.level_info_frame = QFrame()
        self.level_info_frame.setFrameShape(QFrame.StyledPanel)

        level_info_layout = QVBoxLayout(self.level_info_frame)

        self.level_name_label = QLabel("Выберите уровень")
        self.level_name_label.setFont(QFont("Arial", 12, QFont.Bold))

        self.level_desc_label = QLabel("Описание выбранного уровня будет отображаться здесь")
        self.level_desc_label.setWordWrap(True)

        self.level_difficulty_label = QLabel("Сложность: -")

        level_info_layout.addWidget(self.level_name_label)
        level_info_layout.addWidget(self.level_desc_label)
        level_info_layout.addWidget(self.level_difficulty_label)

        main_layout.addWidget(self.level_info_frame)
        main_layout.addSpacing(10)

        # Кнопка "Играть"
        self.play_button = QPushButton("ИГРАТЬ")
        self.play_button.setMinimumHeight(50)
        self.play_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.play_button.setEnabled(False)  # Изначально кнопка неактивна
        main_layout.addWidget(self.play_button)

        # Нижний ряд кнопок
        bottom_buttons_layout = QHBoxLayout()

        settings_button = QPushButton("Настройки")
        credits_button = QPushButton("Авторы")
        quit_button = QPushButton("Выход")

        bottom_buttons_layout.addWidget(settings_button)
        bottom_buttons_layout.addWidget(credits_button)
        bottom_buttons_layout.addWidget(quit_button)

        main_layout.addLayout(bottom_buttons_layout)

        # Подключаем сигналы
        self.levels_list.itemClicked.connect(self.on_level_selected)
        self.play_button.clicked.connect(self.start_game)
        quit_button.clicked.connect(self.close)

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