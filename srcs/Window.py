import pygame
from WindowTheme import WindowTheme
from utils.Colors import *
import os


class Window:
    def __init__(
        self,
        title: str = "Window",
        size: tuple[int, int] = (400, 400),
        theme: WindowTheme = WindowTheme(THEME="blue"),
        font: str = "fonts/Jaro/static/Jaro-Regular.ttf"
    ):
        self.__ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.SCREEN_WIDTH = size[0]
        self.SCREEN_HEIGHT = size[1]
        pygame.init()
        pygame.font.init()
        self.canvas = pygame.display.set_mode(size=size)
        pygame.display.set_caption(title=title)
        print(os.path.join(self.__ROOT_PATH, font))
        # print(font)
        self.fontTitle = pygame.font.Font(os.path.join(self.__ROOT_PATH, font), 64)
        self.exit = False
        self.theme = theme.get()

    def launch(self):
        while self.exit == False:
            self.create_background(pattern_size=64)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            pass
        pass

    def create_background(self, pattern_size: int = 24):
        pattern_bool = 0
        x, y = 0, 0
        while x < self.SCREEN_WIDTH:
            y = 0
            while y < self.SCREEN_HEIGHT:
                pygame.draw.rect(self.canvas, self.theme[f"bg{1 + pattern_bool}"], pygame.Rect(x, y, pattern_size, pattern_size))
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

    def add_text(self, text: str, x: int = None, y: int = None, color: str = "#FFFFFF", shadow: dict = None):
        text_render = self.fontTitle.render(text, True, color)
        if shadow:
            text_shadow = self.fontTitle.render(text, True, shadow['color'])
            text_shadow.set_alpha(shadow['opacity'])

        x_coord = x
        y_coord = y

        text_rect = text_render.get_rect()
        if x == None and y == None:
            x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
            y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)
        elif x == None:
            x_coord = (self.SCREEN_WIDTH / 2) - (text_rect.width / 2)
        elif y == None:
            y_coord = (self.SCREEN_HEIGHT / 2) - (text_rect.height / 2)

        if shadow:
            text_shadow = self.fontTitle.render(text, True, shadow['color'])
            text_shadow.set_alpha(shadow['opacity'])
            self.canvas.blit(text_shadow, [x_coord + shadow['x'], y_coord + shadow['y']])
        self.canvas.blit(text_render, [x_coord, y_coord])

if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
