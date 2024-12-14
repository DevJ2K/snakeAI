import os
import pygame
import pygame.gfxdraw
from WindowTheme import WindowTheme
from srcs.Snake import Snake
from utils import my_cursors
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
        self.SCREEN_WIDTH = size[0]
        self.SCREEN_HEIGHT = size[1]
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.canvas = pygame.display.set_mode(size=size)
        pygame.display.set_caption(title=title)
        # print(font)
        self.fontTitle = pygame.font.Font(os.path.join(ROOT_PATH, font), 64)
        self.fontButton = pygame.font.Font(os.path.join(ROOT_PATH, font), 48)
        self.fontText = pygame.font.Font(os.path.join(ROOT_PATH, font), 24)
        self.run = False
        self.FPS = FPS
        self.tick = 0
        self.last_tick = 0
        self.theme = theme.get()

        self.menu = "MAIN"

        self.snake = Snake(size=10, snake_length=3)
        self.max_len = self.snake.max_snake_length

        self.next_direction = None
        self.speed = 7

        # Window Interface Handling
        self.buttons = []

    def switch_menu(self, menu: str):
        self.menu = menu

    def current_menu(self):
        if self.menu == "MAIN":
            win_screen.MENU_main(self)
        elif self.menu == "GAME_INTERFACE":
            win_screen.GAME_interface(self)
        elif self.menu == "COMPUTOR_MENU":
            win_screen.MENU_computor(self)
        else:
            pass

    def start_new_snake(self):
        old_max_len = self.snake.max_snake_length
        self.max_len = max(self.max_len, old_max_len)
        self.switch_menu("GAME_INTERFACE")
        self.snake = Snake()
        self.snake.max_snake_length = self.max_len

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

    def launch(self):
        self.run = True
        while self.run:
            self.create_background(pattern_size=64)
            self.buttons.clear()
            self.last_tick = self.tick
            self.tick += 1
            self.current_menu()
            onclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_window()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_window()
                    if self.menu == "GAME_INTERFACE":
                        self.handle_gamekey(event.key)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        onclick = True

            if self.menu == "GAME_INTERFACE":
                self.handle_gameloop()
            self.update_button(pygame.mouse.get_pos(), onclick)

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def exit_window(self):
        self.run = False

    def update_button(self, pos: tuple[int, int], onclick: bool = False):
        # {
        #     "text": text,
        #     "x": x,
        #     "y": y,
        #     "color": color,
        #     "bg_color": bg_color,
        #     "stroke": stroke,
        #     "hitbox": button_hitbox,
        #     "func": func
        # }
        # test: pygame.Rect = draw_bordered_rounded_rect()
        final_hover = False
        for button in self.buttons:
            hover = False
            if button['hitbox'].collidepoint(pos):
                cursor_color = self.canvas.get_at(pygame.mouse.get_pos())
                color_list = [
                    pygame.Color(self.theme['bg1']),
                    pygame.Color(self.theme['bg2'])
                ]
                if cursor_color not in color_list:
                    # print(f"Collisions with {button['text']}")
                    hover = True
                    final_hover = True
                    if onclick:
                        if button['func_params']:
                            button['func'](button['func_params'])
                        else:
                            button['func']()

            win_utils.add_button(
                window,
                button['text'],
                button['x'],
                button['y'],
                button['font'],
                button['color'],
                button['bg_default'],
                button['bg_hover'],
                button['stroke'],
                button['border_radius'],
                button['func'],
                button['func_params'],
                hover,
                False,
            )
        if final_hover:
            # pygame.mouse.set_cursor(pygame.cursors.tri_left)
            hover_cursor = pygame.cursors.compile(my_cursors.hover_strings)
            pygame.mouse.set_cursor((24, 16), (0, 0), *hover_cursor)
        else:
            pygame.mouse.set_cursor(pygame.cursors.arrow)

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
            pygame.draw.rect(
                self.canvas,
                item['hex'],
                pygame.Rect(x, y, TILE_X, TILE_Y)
            )
        elif item['name'] == "EMPTY_SPACE":
            pygame.draw.rect(
                self.canvas,
                self.theme[f"board{1 + pattern_bool}"],
                pygame.Rect(x, y, TILE_X, TILE_Y)
            )
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
                    self.draw_on_board(x, y, TILE_X, TILE_Y, item, bg_pattern)
                    # pygame.draw.rect(
                    #     self.canvas,
                    #     self.theme[f"board{1 + pattern_bool}"],
                    #     pygame.Rect(x, y, TILE_X, TILE_Y)
                    # )
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


if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
