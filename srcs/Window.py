import pygame
import pygame.gfxdraw
from WindowTheme import WindowTheme
from srcs.Snake import Snake
from utils.pygame_utils import draw_bordered_rounded_rect
from utils import my_cursors
from window.window_menu import MENU_main
import os


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
            MENU_main(self)
        elif self.menu == "GAME_INTERFACE":
            self.GAME_interface()
        elif self.menu == "COMPUTOR_MENU":
            self.MENU_computor()
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
        if self.snake.game_over is True:
            return

        head = self.snake.snake[0]
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

            self.add_button(
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

        self.add_text(
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

    def add_image(
        self,
        filename: str,
        x: int = None,
        y: int = None,
        width: int = None,
        height: int = None
    ):
        tmp_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        img = pygame.image.load(os.path.join(tmp_path, "images", filename))

        x_coord = x
        y_coord = y

        img_rect = img.get_rect()
        if x is None and y is None:
            x_coord = (self.SCREEN_WIDTH / 2) - (img_rect.width / 2)
            y_coord = (self.SCREEN_HEIGHT / 2) - (img_rect.height / 2)
        elif x is None:
            x_coord = (self.SCREEN_WIDTH / 2) - (img_rect.width / 2)
        elif y is None:
            y_coord = (self.SCREEN_HEIGHT / 2) - (img_rect.height / 2)

        width = img_rect.width if width is None else width
        height = img_rect.height if height is None else height

        img = pygame.transform.scale(img, (width, height))

        self.canvas.blit(img, pygame.Rect(x_coord, y_coord, width, height))

    def add_text(
            self,
            text: str,
            x: int = None,
            y: int = None,
            color: str = "#FFFFFF",
            shadow: dict = None,
            font: pygame.font.Font = None
    ):
        if font is None:
            font = self.fontText
        text_render = font.render(text, True, color)
        x_coord = x
        y_coord = y

        text_rect = text_render.get_rect()
        if x is None and y is None:
            x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
            y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)
        elif x is None:
            x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
        elif y is None:
            y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)

        if shadow:
            text_shadow = font.render(text, True, shadow['color'])
            text_shadow.set_alpha(shadow['opacity'])
            shadow_x = x_coord + shadow['x']
            shadow_y = y_coord + shadow['y']
            self.canvas.blit(text_shadow, [shadow_x, shadow_y])
        self.canvas.blit(text_render, [x_coord, y_coord])

    def add_button(
            self,
            text: str,
            x: int = None,
            y: int = None,
            font: pygame.font.Font = None,
            color: str = "#FFFFFF",
            bg_default: str = "#000000",
            bg_hover: str = "#4F4F4F",
            stroke: str = "#FFFFFF",
            border_radius: int = 32,
            func: callable = print,
            func_params: tuple = None,
            hover: bool = False,
            append: bool = True
    ):

        # Padding var
        px = 32
        py = 12
        if font is None:
            font = self.fontButton
        text_render = font.render(text, True, color)
        x_coord = x
        y_coord = y

        bg_color = bg_hover if hover is True else bg_default
        text_rect = text_render.get_rect()
        if x is None and y is None:
            x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
            y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)
        elif x is None:
            x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
        elif y is None:
            y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)

        # rect_bg = pygame.draw.rect(self.canvas, bg_color, pygame.Rect(
        #     x_coord - px, y_coord - py,
        #     text_rect.width + (px * 2),
        #     text_rect.height + (py * 2)),
        #     0,
        #     64
        # )

        # def draw_circle(surface, x, y, radius, color):
        #     gfxdraw.aacircle(surface, x, y, radius, color)
        #     gfxdraw.filled_circle(surface, x, y, radius, color)

        button_rect = pygame.Rect(
            x_coord - px, y_coord - py,
            text_rect.width + (px * 2),
            text_rect.height + (py * 2))

        draw_bordered_rounded_rect(
            self.canvas,
            button_rect,
            pygame.Color(bg_color),
            pygame.Color(stroke),
            border_radius,
            5
        )
        # while True:
        #     try:
        #         break
        #     except:
        #         border_radius -= 8
        # print(border_radius)

        if append:
            self.buttons.append(
                {
                    "text": text,
                    "x": x,
                    "y": y,
                    "color": color,
                    "font": font,
                    "bg_default": bg_default,
                    "bg_hover": bg_hover,
                    "stroke": stroke,
                    "border_radius": border_radius,
                    "hitbox": button_rect,
                    "func": func,
                    "func_params": func_params
                }
            )

        self.canvas.blit(text_render, [x_coord, y_coord])

    def MENU_main(self):
        self.add_button(
            text="PLAY",
            y=self.SCREEN_HEIGHT / 2 - 140,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.start_new_snake,
            func_params=None
        )
        self.add_button(
            text="COMPUTOR",
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.switch_menu,
            func_params="COMPUTOR_MENU"
        )

        self.add_button(
            text="LEAVE",
            y=self.SCREEN_HEIGHT / 2 + 80,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.exit_window
        )

    def MENU_computor(self):
        self.add_button(
            text="VISUALIZATION",
            y=self.SCREEN_HEIGHT / 2 - 140,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.start_new_snake,
            func_params=None
        )
        self.add_button(
            text="TRAINING",
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.start_new_snake,
            func_params=None
        )

        self.add_button(
            text="BACK",
            y=self.SCREEN_HEIGHT / 2 + 80,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.switch_menu,
            func_params="MAIN"
        )
        pass

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
        x_center = self.SCREEN_WIDTH / 2
        self.add_image("len.png", x_center - 160, y, 48, 32)
        self.add_text(str(self.snake.snake_length), x_center - 100, y)

        self.add_image("timer.png", x_center - 40, y, 32, 32)
        self.add_text(f"{self.snake.get_timer():.2f}s", x_center + 2, y)

        self.add_image("trophy.png", x_center + 100, y, 32, 32)
        self.add_text(str(self.snake.max_snake_length), x_center + 144, y)

    def GAME_interface(self):

        draw_snake = self.snake.game_over is False
        value = self.create_snakeboard(self.snake.size, draw_snake)
        x_size, y_size, x_start, y_start = value
        if self.snake.is_running is False and self.snake.game_over is False:
            self.add_text("Press any direction to start", y=120)
        elif self.snake.is_running is False and self.snake.game_over is True:
            pygame.draw.rect(
                self.canvas,
                self.theme['board2'],
                pygame.Rect(x_start, y_start, x_size, y_size)
            )
            self.add_text("Game is over !", y=120)

            self.add_text(
                "Stats",
                y=self.SCREEN_HEIGHT / 2 - 88,
                font=self.fontButton,
                shadow={
                    "color": self.theme['accent'],
                    "opacity": 42,
                    "x": 4,
                    "y": 4,
                })
            self.display_game_info(y=self.SCREEN_HEIGHT / 2 - 20)
            self.add_button(
                "REPLAY",
                y=self.SCREEN_HEIGHT / 2 + 42,
                font=self.fontText,
                bg_default=self.theme['btn'],
                bg_hover=self.theme['btn-hover'],
                border_radius=16,
                func=self.start_new_snake,
                func_params=None
            )
        else:
            self.display_game_info(y=120)
        self.add_button(
            text="LEAVE",
            y=self.SCREEN_HEIGHT - 100,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.leave_game
        )


if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
