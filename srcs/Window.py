import pygame
import pygame.gfxdraw
from WindowTheme import WindowTheme
# from utils.Colors import *
from utils.pygame_utils import draw_bordered_rounded_rect
from utils import my_cursors
import os
import math


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
        self.run = False
        self.FPS = FPS
        self.theme = theme.get()

        self.menu = "GAME_INTERFACE"

        # Window Interface Handling
        self.buttons = []

    def switch_menu(self, menu: str):
        self.menu = menu

    def current_menu(self):
        if self.menu == "MAIN":
            self.MENU_main()
        elif self.menu == "GAME_INTERFACE":
            self.GAME_interface()
        else:
            pass

    def launch(self):
        # i = 0
        self.run = True
        while self.run:
            self.create_background(pattern_size=64)
            self.buttons.clear()
            # print(i)
            # i += 1
            # self.menu_select()
            self.current_menu()
            onclick = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_window()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_window()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        onclick = True

            self.update_button(pygame.mouse.get_pos(), onclick)

            pygame.display.update()
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
                button['color'],
                button['bg_default'],
                button['bg_hover'],
                button['stroke'],
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
                "color": "#0000FF",
                "opacity": 42,
                "x": 4,
                "y": 4,
            }
        )

    def add_text(
            self,
            text: str,
            x: int = None,
            y: int = None,
            color: str = "#FFFFFF",
            shadow: dict = None
    ):
        text_render = self.fontTitle.render(text, True, color)
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
            text_shadow = self.fontTitle.render(text, True, shadow['color'])
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
            color: str = "#FFFFFF",
            bg_default: str = "#000000",
            bg_hover: str = "#4F4F4F",
            stroke: str = "#FFFFFF",
            func: callable = print,
            func_params: tuple = None,
            hover: bool = False,
            append: bool = True
    ):

        # Padding var
        px = 32
        py = 12
        text_render = self.fontButton.render(text, True, color)
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
            32,
            5
        )

        if append:
            self.buttons.append(
                {
                    "text": text,
                    "x": x,
                    "y": y,
                    "color": color,
                    "bg_default": bg_default,
                    "bg_hover": bg_hover,
                    "stroke": stroke,
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
            func=self.switch_menu,
            func_params="GAME_INTERFACE"
        )

        self.add_button(
            text="LEAVE",
            y=self.SCREEN_HEIGHT / 2,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.exit_window
        )


    def create_snakeboard(self, size: int = 10):
        # Create game board border
        DEFAULT_WIDTH = 400
        DEFAULT_HEIGHT = 400
        BORDER_SIZE = 6


        # text_rect = text_render.get_rect()
        # if x is None and y is None:
        #     x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
        #     y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)

        WIDTH = DEFAULT_WIDTH - (2 * BORDER_SIZE)
        HEIGHT = DEFAULT_HEIGHT - (2 * BORDER_SIZE)
        TILE_X = round(WIDTH / size)
        TILE_Y = round(HEIGHT / size)

        y = self.SCREEN_HEIGHT / 2 - (HEIGHT / 2)
        pattern_bool = 0
        for _ in range(size):
            x = self.SCREEN_WIDTH / 2 - (WIDTH / 2)
            for __ in range(size):
                pattern_bool = 1 - pattern_bool
                pygame.draw.rect(
                    self.canvas,
                    self.theme[f"board{1 + pattern_bool}"],
                    pygame.Rect(x, y, TILE_X, TILE_Y)
                )
                x += TILE_X
            if size % 2 == 0:
                pattern_bool = 1 - pattern_bool
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

    def GAME_interface(self):
        self.create_snakeboard(size=10)
        self.add_button(
            text="LEAVE",
            y=self.SCREEN_HEIGHT - 100,
            bg_default=self.theme['btn'],
            bg_hover=self.theme['btn-hover'],
            func=self.switch_menu,
            func_params="MAIN"
        )


if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
