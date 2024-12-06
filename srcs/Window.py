import pygame
import pygame.gfxdraw
from WindowTheme import WindowTheme
# from utils.Colors import *
from utils.pygame_utils import draw_bordered_rounded_rect
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
        self.run = False
        self.FPS = FPS
        self.theme = theme.get()

        # Window Interface Handling
        self.buttons = []

    def launch(self):
        # i = 0
        while not self.run:
            self.create_background(pattern_size=64)
            self.buttons.clear()
            # print(i)
            # i += 1
            self.main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = True
                    print(event.dict)

            self.update_button_hover(pygame.mouse.get_pos())

            pygame.display.update()
            self.clock.tick(self.FPS)

    def update_button_hover(self, pos: tuple[int, int]):
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
        for button in self.buttons:
            if button['hitbox'].collidepoint(pos):
                cursor_color = self.canvas.get_at(pygame.mouse.get_pos())
                color_list = [
                    pygame.Color(button['color']),
                    pygame.Color(button['bg_color']),
                    pygame.Color(button['stroke'])
                ]
                if cursor_color in color_list:
                    print(f"Collisions with {button['text']}")
        pass

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

    def main_menu(self):
        self.add_button(
            text="PLAY",
            y=self.SCREEN_HEIGHT / 2 - 140,
            bg_color="#0000FF"
        )
        self.add_button(
            text="LEAVE",
            y=self.SCREEN_HEIGHT / 2,
            bg_color="#0000FF"
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
            bg_color: str = "#000000",
            stroke: str = "#FFFFFF",
            func: callable = print,
            append: bool = True
    ):

        # Padding var
        px = 32
        py = 12
        text_render = self.fontButton.render(text, True, color)
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
                    "bg_color": bg_color,
                    "stroke": stroke,
                    "hitbox": button_rect,
                    "func": func
                }
            )

        self.canvas.blit(text_render, [x_coord, y_coord])


if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
