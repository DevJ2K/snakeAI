import pygame
import pygame.gfxdraw
from WindowTheme import WindowTheme
from utils.Colors import *
import os
import pygame.gfxdraw

def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

def draw_bordered_rounded_rect(surface, rect, color, border_color, corner_radius, border_thickness):
    if corner_radius < 0:
        raise ValueError(f"border radius ({corner_radius}) must be >= 0")

    rect_tmp = pygame.Rect(rect)
    center = rect_tmp.center

    if border_thickness:
        if corner_radius <= 0:
            pygame.draw.rect(surface, border_color, rect_tmp)
        else:
            draw_rounded_rect(surface, rect_tmp, border_color, corner_radius)

        rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
        inner_radius = corner_radius - border_thickness + 1
    else:
        inner_radius = corner_radius

    if inner_radius <= 0:
        pygame.draw.rect(surface, color, rect_tmp)
    else:
        draw_rounded_rect(surface, rect_tmp, color, inner_radius)

class Window:
    def __init__(
        self,
        title: str = "Window",
        size: tuple[int, int] = (400, 400),
        theme: WindowTheme = WindowTheme(THEME="blue"),
        font: str = "fonts/Jaro/static/Jaro-Regular.ttf",
        FPS: int = 60
    ):
        self.__ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.SCREEN_WIDTH = size[0]
        self.SCREEN_HEIGHT = size[1]
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.canvas = pygame.display.set_mode(size=size)
        pygame.display.set_caption(title=title)
        print(os.path.join(self.__ROOT_PATH, font))
        # print(font)
        self.fontTitle = pygame.font.Font(os.path.join(self.__ROOT_PATH, font), 64)
        self.fontButton = pygame.font.Font(os.path.join(self.__ROOT_PATH, font), 48)
        self.run = False
        self.FPS = FPS
        self.theme = theme.get()

    def launch(self):
        # i = 0
        while self.run == False:
            self.clock.tick(self.FPS)
            self.create_background(pattern_size=64)
            # print(i)
            # i += 1
            self.main_menu()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = True
                if event.type == pygame.KEYDOWN:
                    print(event.dict)


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


    def add_text(self, text: str, x: int = None, y: int = None, color: str = "#FFFFFF", shadow: dict = None):
        text_render = self.fontTitle.render(text, True, color)
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

    def add_button(self, text: str, x: int = None, y: int = None, color: str = "#FFFFFF", bg_color: str = "#000000", stroke: str = "#FFFFFF"):

        # Padding var
        px = 32
        py = 12
        text_render = self.fontButton.render(text, True, color)
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

        rect_bg = pygame.draw.rect(self.canvas, bg_color, pygame.Rect(x_coord - px, y_coord - py, text_rect.width + (px * 2), text_rect.height + (py * 2)), 0, 64)


        # def draw_circle(surface, x, y, radius, color):
        #     gfxdraw.aacircle(surface, x, y, radius, color)
        #     gfxdraw.filled_circle(surface, x, y, radius, color)


        # stroke_bg = pygame.draw.rect(self.canvas, stroke, pygame.Rect(x_coord - px, y_coord - py, text_rect.width + (px * 2), text_rect.height + (py * 2)), 5, 64)
        draw_bordered_rounded_rect(self.canvas, pygame.Rect(x_coord - px, y_coord - py, text_rect.width + (px * 2), text_rect.height + (py * 2)), pygame.Color(0, 0, 255), pygame.Color(255, 255, 255), 32, 5)
        self.canvas.blit(text_render, [x_coord, y_coord])

if __name__ == "__main__":
    window = Window(title="SnakeAI", size=(1000, 800))
    window.launch()
