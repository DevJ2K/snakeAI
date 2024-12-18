import os
import pygame
import platform
import pygame.gfxdraw
from WindowTheme import WindowTheme
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(sys.path)

from srcs.Snake import Snake
from srcs.Training import Training
import window.window_menu as win_screen
import window.window_utils as win_utils


class Window:
    def __init__(
        self,
        title: str = "Window",
        size: tuple[int, int] = (400, 400),
        theme: WindowTheme = WindowTheme(THEME="blue"),
        font: str = "fonts/Jaro/static/Jaro-Regular.ttf",
        FPS: int = 60
    ):
        abs_file_path = os.path.abspath(__file__)
        ROOT_PATH = os.path.dirname(os.path.dirname(abs_file_path))
        self.font = font
        self.ROOT_PATH = ROOT_PATH
        self.SCREEN_WIDTH = size[0]
        self.SCREEN_HEIGHT = size[1]
        self.MAX_SESSIONS = 9999
        # print(platform.system())
        if platform.system() == "Darwin":
            self.tk = Tk()
            self.tk.withdraw()
            pygame.init()
        else:
            pygame.init()
            self.tk = Tk()
            self.tk.withdraw()

        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.canvas = pygame.display.set_mode(size=size)
        pygame.display.set_caption(title=title)
        # print(font)
        self.fontTitle = pygame.font.Font(
            os.path.join(self.ROOT_PATH, font), 64)
        self.fontButton = pygame.font.Font(
            os.path.join(self.ROOT_PATH, font), 48)
        self.fontText = pygame.font.Font(
            os.path.join(self.ROOT_PATH, font), 24)
        self.run = False
        self.FPS = FPS
        self.tick = 0
        self.last_tick = 0
        self.theme = theme.get()

        self.menu = "COMPUTOR_TRAINING_SETTINGS"

        self.snake = Snake(size=10, snake_length=3)
        self.training = Training(
            board_size=10,
            sessions_number=1,
            model=None,
            learn=False
        )
        self.max_len = self.snake.max_snake_length

        self.next_direction = None
        self.speed = 7

        # Window Interface Handling
        self.buttons = []
        self.triangle_buttons = []

        self.is_editing_session_num: bool = False
        self.session_num_display: str = str(self.training.sessions_number)

    def get_font(self, size: int) -> pygame.font.Font:
        return pygame.font.Font(os.path.join(self.ROOT_PATH, self.font), size)

    def switch_menu(self, menu: str):
        self.menu = menu

    def current_menu(self):
        if self.menu == "MAIN":
            win_screen.MENU_main(self)
        elif self.menu == "GAME_INTERFACE":
            win_screen.GAME_interface(self)
        elif self.menu == "COMPUTOR_MENU":
            win_screen.MENU_computor(self)
        elif self.menu == "COMPUTOR_VISUALIZATION_SETTINGS":
            win_screen.MENU_computor_visualization(self)
        elif self.menu == "COMPUTOR_TRAINING_SETTINGS":
            win_screen.MENU_computor_training(self)
        elif self.menu == "TRAINING_VISUALIZATION":
            win_screen.RUN_training_visualization(self)
        else:
            print(f"No menu select. '{self.menu}'")
            pass

    def start_new_snake(self):
        old_max_len = self.snake.max_snake_length
        self.max_len = max(self.max_len, old_max_len)
        self.switch_menu("GAME_INTERFACE")
        self.snake = Snake()
        self.snake.max_snake_length = self.max_len

    def run_training(self):
        self.switch_menu("TRAINING_VISUALIZATION")

    def handle_gameloop(self):
        tick = (self.tick * self.speed) % self.FPS
        last_tick = (self.last_tick * self.speed) % self.FPS
        if self.snake.is_running is False:
            return
        if self.next_direction is None:
            return
        if tick < last_tick:
            if self.snake.next_frame(self.next_direction) is False:
                self.handle_gameover()
                self.snake.is_running = False
        # print(tick)

    def leave_game(self):
        self.snake = Snake()
        self.switch_menu("MAIN")

    def handle_gameover(self):
        if self.snake.is_running is True:
            self.snake.game_over = True
            self.snake.is_running = False
            self.snake.end_timer()

    def handle_gamekey(self, key):
        head = self.snake.snake[0]
        if window.snake.is_running is False and window.snake.game_over is True:
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self.start_new_snake()
        if self.snake.game_over is True:
            return
        if key == pygame.K_UP and head.direction != self.snake.DOWN:
            self.next_direction = self.snake.UP
        elif key == pygame.K_DOWN and head.direction != self.snake.UP:
            self.next_direction = self.snake.DOWN
        elif key == pygame.K_LEFT and head.direction != self.snake.RIGHT:
            self.next_direction = self.snake.LEFT
        elif key == pygame.K_RIGHT and head.direction != self.snake.LEFT:
            self.next_direction = self.snake.RIGHT
        else:
            return
        if self.snake.is_running is False:
            self.snake.is_running = True
            self.snake.start_timer()

    def handle_session_typing(self, key):
        if key == pygame.K_ESCAPE or key == pygame.K_RETURN:
            self.is_editing_session_num = False
            if self.session_num_display == "...":
                self.session_num_display = "1"
            self.training.sessions_number = int(self.session_num_display)

        if key == pygame.K_BACKSPACE:
            if self.session_num_display == "...":
                return
            new_number = int(self.session_num_display) // 10
            if new_number <= 0:
                self.session_num_display = "..."
            else:
                self.session_num_display = str(new_number)

        if 48 <= key and key <= 57:
            number = int(chr(key))
            if self.session_num_display == "...":
                if number != 0:
                    self.session_num_display = str(number)
            else:
                new_number = int(self.session_num_display) * 10 + number
                # print(int(self.session_num_display) * 10, number)
                if new_number >= self.MAX_SESSIONS:
                    new_number = self.MAX_SESSIONS
                    self.session_num_display = str(new_number)
                elif new_number <= 0:
                    self.session_num_display = "..."
                else:
                    self.session_num_display = str(new_number)

    def launch(self):
        self.run = True
        while self.run:
            self.create_background(pattern_size=64)
            self.buttons.clear()
            self.triangle_buttons.clear()
            self.last_tick = self.tick
            self.tick += 1
            self.current_menu()
            onclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_window()
                if event.type == pygame.KEYDOWN:
                    is_editing = self.is_editing_session_num is True
                    if event.key == pygame.K_ESCAPE and is_editing is False:
                        self.exit_window()
                    if self.menu == "GAME_INTERFACE":
                        self.handle_gamekey(event.key)
                    if self.is_editing_session_num is True:
                        self.handle_session_typing(event.key)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.is_editing_session_num is True:
                            self.handle_session_typing(pygame.K_ESCAPE)
                        else:
                            onclick = True

            if self.menu == "GAME_INTERFACE":
                self.handle_gameloop()
            win_utils.update_button(self, pygame.mouse.get_pos(), onclick)

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def exit_window(self):
        self.run = False

    def create_background(self, pattern_size: int = 24):
        pattern_bool = 0
        x, y = 0, 0
        while x < self.SCREEN_WIDTH:
            y = 0
            while y < self.SCREEN_HEIGHT:
                pygame.draw.rect(
                    self.canvas,
                    self.theme[f"bg{1 + pattern_bool}"],
                    pygame.Rect(x, y, pattern_size, pattern_size)
                )
                pattern_bool = 1 - pattern_bool

                y += pattern_size

            x += pattern_size

        win_utils.add_text(
            window,
            text="SNAKE",
            y=32,
            color="#FFFFFF",
            shadow={
                "color": self.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
            },
            font=self.fontTitle
        )

    def draw_on_board(
            self,
            x: int,
            y: int,
            TILE_X: int,
            TILE_Y: int,
            item: dict,
            pattern_bool: int = 0
    ):

        if item['name'] in ["HEAD", "SNAKE_BODY"]:

            pygame.draw.rect(
                self.canvas,
                item['hex'],
                pygame.Rect(x, y, TILE_X, TILE_Y)
            )
        elif item['name'] in ["GREEN_APPLE", "RED_APPLE"]:
            px = 6
            py = 6
            pygame.draw.rect(
                self.canvas,
                item['hex'],
                pygame.Rect(x + px / 2, y + py / 2, TILE_X - px, TILE_Y - py),
                0,
                border_bottom_left_radius=16,
                border_bottom_right_radius=16,
                border_top_left_radius=12,
                border_top_right_radius=12
            )
        elif item['name'] == "EMPTY_SPACE":
            pass
            # pygame.draw.rect(
            #     self.canvas,
            #     self.theme[f"board{1 + pattern_bool}"],
            #     pygame.Rect(x, y, TILE_X, TILE_Y)
            # )
        else:
            pygame.draw.rect(
                self.canvas,
                "#1F1F1F",
                pygame.Rect(x, y, TILE_X, TILE_Y)
            )

    def create_snakeboard(self, size: int = 10, draw_snake: bool = True):
        # Create game board border
        DEFAULT_WIDTH = 400
        DEFAULT_HEIGHT = 400
        BORDER_SIZE = 6

        WIDTH = DEFAULT_WIDTH - (2 * BORDER_SIZE)
        HEIGHT = DEFAULT_HEIGHT - (2 * BORDER_SIZE)
        TILE_X = round(WIDTH / size)
        TILE_Y = round(HEIGHT / size)

        start_x = self.SCREEN_WIDTH / 2 - (WIDTH / 2)
        start_y = self.SCREEN_HEIGHT / 2 - (HEIGHT / 2)

        y = self.SCREEN_HEIGHT / 2 - (HEIGHT / 2)
        bg_pattern = 0
        if draw_snake:
            for i in range(size):
                x = self.SCREEN_WIDTH / 2 - (WIDTH / 2)
                for j in range(size):
                    bg_pattern = 1 - bg_pattern
                    char = self.snake.get_board_without_border()[i][j]
                    item = self.snake.get_item_by_char(char)
                    pygame.draw.rect(
                        self.canvas,
                        self.theme[f"board{1 + bg_pattern}"],
                        pygame.Rect(x, y, TILE_X, TILE_Y)
                    )
                    self.draw_on_board(x, y, TILE_X, TILE_Y, item, bg_pattern)
                    x += TILE_X
                if size % 2 == 0:
                    bg_pattern = 1 - bg_pattern
                y += TILE_Y

        # outline_border
        pygame.draw.rect(self.canvas, pygame.Color(255, 255, 255), pygame.Rect(
            self.SCREEN_WIDTH / 2 - (DEFAULT_WIDTH / 2) - (BORDER_SIZE),
            self.SCREEN_HEIGHT / 2 - (DEFAULT_HEIGHT / 2) - (BORDER_SIZE),
            DEFAULT_WIDTH + (BORDER_SIZE * 2),
            DEFAULT_HEIGHT + (BORDER_SIZE * 2)),
            BORDER_SIZE,
            16
        )
        # inline_border
        pygame.draw.rect(self.canvas, pygame.Color(255, 255, 255), pygame.Rect(
            self.SCREEN_WIDTH / 2 - (DEFAULT_WIDTH / 2),
            self.SCREEN_HEIGHT / 2 - (DEFAULT_HEIGHT / 2),
            DEFAULT_WIDTH,
            DEFAULT_HEIGHT),
            BORDER_SIZE,
            0
        )
        return (TILE_X * size, TILE_Y * size, start_x, start_y)

    def display_game_info(self, y: int):
        x = self.SCREEN_WIDTH / 2
        win_utils.add_image(window, "len.png", x - 160, y, 48, 32)
        win_utils.add_text(window, str(self.snake.snake_length), x - 100, y)

        win_utils.add_image(window, "timer.png", x - 40, y, 32, 32)
        win_utils.add_text(window, f"{self.snake.get_timer():.2f}s", x + 2, y)

        win_utils.add_image(window, "trophy.png", x + 100, y, 32, 32)
        tmp_x = x + 144
        win_utils.add_text(window, str(self.snake.max_snake_length), tmp_x, y)

    def get_model(self):
        # print(f"Calling loop {self.clock}")
        return str(self.training.model)

    def select_model(self):
        # HANDLE MACOS
        # from magicgui.backends._qtpy import show_file_dialog
        # from PySide6 import QtCore, QtWidgets, QtGui
        # app = QtWidgets.QApplication([])
        # filename = str(show_file_dialog())
        # # sys.exit(app.exec())
        # app.shutdown()
        # print(filename)
        # return
        # tmp_win = Tk()
        # tmp_win.withdraw()
        # tmp_win.tk.call('tk', 'scaling', 2.0)
        # filename = askopenfilename(title="Select a model")
        filename = askopenfilename(title="Select a model")
        # print(filename)
        if filename.isinstance(list) or filename.isinstance(tuple):
            if len(filename) > 0:
                filename = filename[0]
            else:
                filename = ''
        # print(platform.system())
        # filename = "empty"
        self.buttons.clear()
        # tmp_win.destroy()
        if filename == '':
            return
        else:
            self.training.model = filename

    def decrease_board_size(self):
        if self.training.board_size == 10:
            return
        else:
            self.training.board_size -= 2

    def increase_board_size(self):
        if self.training.board_size == 20:
            return
        else:
            self.training.board_size += 2

    def edit_sessions_number(self):
        self.is_editing_session_num = True
        self.session_num_display = "..."


if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
