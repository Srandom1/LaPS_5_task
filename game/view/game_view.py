import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenuBar,
    QGraphicsView,
    QGraphicsScene,
    QAction,
    QMessageBox
)

from game.controllers.game_controller import GameController
from game.controllers.player_controller import PlayerController
from game.models.models import *
from game.models.field import Field
from game.viewModels.view_models import *


class GameWindow(QMainWindow):
    def __init__(self, main_menu,
                 field: Field, player_controller:PlayerController, game_controller: GameController):
        super().__init__()
        self.menu = main_menu
        self.player_controller = player_controller
        self.game_controller = game_controller
        self.field = field
        self._cells_view_models = []

        self._init_scene()
        self._init_cells_view_models()
        self._fill_scene_with_cells()



    def _init_scene(self):
        self._scene = QGraphicsScene(self)
        self._view = QGraphicsView(self._scene)

        # Настройка представления
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._view.setRenderHint(QPainter.Antialiasing)
        self._view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

        # Размер ячейки по умолчанию
        self.cell_size = 60

        self.setWindowTitle("Игра")
        self.setGeometry(100, 100, 1200, 800)
        self.setCentralWidget(self._view)

        self._menu_bar = self.menuBar()
        self._create_menu()

        # Обновляем сцену
        self._scene.update()

    def _init_cells_view_models(self):
        cell_matrix = self.field.cell_matrix
        for row_index, row in enumerate(cell_matrix):
            current_row = list()
            self._cells_view_models.append(current_row)
            for col_index, cell in enumerate(row):
                cell_view = CellView(cell)
                cell_view.size = self.cell_size
                current_row.append(cell_view)

    def _fill_scene_with_cells(self):
        for row_index, row in enumerate(self._cells_view_models):
            for col_index, cell in enumerate(row):
                cell_item = self._cells_view_models[row_index][col_index]
                # Размещаем элемент на сцене с заданными координатами
                cell_item.setPos(col_index * self.cell_size, row_index * self.cell_size)
                self._scene.addItem(cell_item)
                cell_item.revalidate()


        scene_rect = QRectF(0, 0,
                           self.field.y_size * self.cell_size,
                            self.field.x_size * self.cell_size)
        self._scene.setSceneRect(scene_rect)

        self._view.fitInView(scene_rect, Qt.KeepAspectRatio)

    def keyPressEvent(self, event):
        if animation_manager.is_animating:
            return
        x = self.player_controller.player.x
        y = self.player_controller.player.y
        direction_vector = Coordinates(0,0)
        if event.key() == Qt.Key_W:
            action_result = self.player_controller.move_up()
            direction_vector.y -= 1
        elif event.key() == Qt.Key_A:
            action_result = self.player_controller.move_left()
            direction_vector.x -= 1
        elif event.key() == Qt.Key_S:
            action_result = self.player_controller.move_down()
            direction_vector.y += 1
        elif event.key() == Qt.Key_D:
            action_result = self.player_controller.move_right()
            direction_vector.x += 1
        else:
            return
        if not action_result:
            self._cells_view_models[y][x].revalidate()
            return
        direction = self.player_controller.player.camera_direction
        current_cell = self._cells_view_models[y][x]
        next_cell = self._cells_view_models[y + direction_vector.y][x + direction_vector.x]
        next_next_cell = self._cells_view_models[y + 2 * direction_vector.y][x + 2* direction_vector.x]
        current_cell.animate(direction, next_cell.revalidate)
        # Будет работать, так как если в следующей клетки нет коробки то просто ничего не произойдет
        next_cell.animate(direction, next_next_cell.revalidate)
        #next_next_cell.animate(direction, next_next_cell.revalidate)

        current_cell.revalidate()
        if not self.game_controller.is_running:
            self.show_win_message()

    def resizeEvent(self, event):
        """Масштабируем представление при изменении размера окна"""
        super().resizeEvent(event)
        self._view.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)

    def _create_menu(self):
        file_menu = self._menu_bar.addMenu("Меню")

        help_action = QAction("Помощь", self)
        help_action.triggered.connect(self.show_help)
        file_menu.addAction(help_action)

        main_menu_action = QAction("Выйти в главное меню", self)
        main_menu_action.triggered.connect(self.exit_to_main_menu)
        file_menu.addAction(main_menu_action)

        exit_action = QAction("Выйти из игры", self)
        exit_action.triggered.connect(self.exit_game)
        file_menu.addAction(exit_action)

    def show_help(self):
        QMessageBox.information(self, "Помощь", "Для перемещения вверх, вниз, вправа, влево изпользуйте wasd")

    def show_win_message(self):
        QMessageBox.information(self, "Приз", "Ура, вы победили")
    def exit_to_main_menu(self):
        self.menu.show()
        self.close()

    def exit_game(self):
        self.close()


if __name__ == "__main__":
    import game.parser as parser
    from game.utils import read_file_as_string


    app = QApplication(sys.argv)
    Icons.set_icons()

    source = read_file_as_string(LEVELS_PATH +  "/" + "level_chil.txt")
    field = parser.generate_field_from_string(source)
    player = Player(None)
    game_controller = GameController(field, player)
    player_controller = PlayerController(player, game_controller)
    game_window = GameWindow(field, player_controller)
    game_window.show()
    sys.exit(app.exec_())
