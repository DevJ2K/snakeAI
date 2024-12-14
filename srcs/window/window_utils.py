# from Window import Window
from utils.pygame_utils import draw_bordered_rounded_rect
import pygame
import os


def add_button(
        window,
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
        font = window.fontButton
    text_render = font.render(text, True, color)
    x_coord = x
    y_coord = y

    bg_color = bg_hover if hover is True else bg_default
    text_rect = text_render.get_rect()
    if x is None and y is None:
        x_coord = (window.SCREEN_WIDTH / 2) - (text_rect.width / 2)
        y_coord = (window.SCREEN_HEIGHT / 2) - (text_rect.height / 2)
    elif x is None:
        x_coord = (window.SCREEN_WIDTH / 2) - (text_rect.width / 2)
    elif y is None:
        y_coord = (window.SCREEN_HEIGHT / 2) - (text_rect.height / 2)

    button_rect = pygame.Rect(
        x_coord - px, y_coord - py,
        text_rect.width + (px * 2),
        text_rect.height + (py * 2))

    draw_bordered_rounded_rect(
        window.canvas,
        button_rect,
        pygame.Color(bg_color),
        pygame.Color(stroke),
        border_radius,
        5
    )

    if append:
        window.buttons.append(
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

    window.canvas.blit(text_render, [x_coord, y_coord])


def add_image(
    window,
    filename: str,
    x: int = None,
    y: int = None,
    width: int = None,
    height: int = None
):
    tmp_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tmp_path = os.path.dirname(tmp_path)

    img = pygame.image.load(os.path.join(tmp_path, "images", filename))

    x_coord = x
    y_coord = y

    img_rect = img.get_rect()
    if x is None and y is None:
        x_coord = (window.SCREEN_WIDTH / 2) - (img_rect.width / 2)
        y_coord = (window.SCREEN_HEIGHT / 2) - (img_rect.height / 2)
    elif x is None:
        x_coord = (window.SCREEN_WIDTH / 2) - (img_rect.width / 2)
    elif y is None:
        y_coord = (window.SCREEN_HEIGHT / 2) - (img_rect.height / 2)

    width = img_rect.width if width is None else width
    height = img_rect.height if height is None else height

    img = pygame.transform.scale(img, (width, height))

    window.canvas.blit(img, pygame.Rect(x_coord, y_coord, width, height))


def add_text(
        window,
        text: str,
        x: int = None,
        y: int = None,
        color: str = "#FFFFFF",
        shadow: dict = None,
        font: pygame.font.Font = None
):
    if font is None:
        font = window.fontText
    text_render = font.render(text, True, color)
    x_coord = x
    y_coord = y

    text_rect = text_render.get_rect()
    if x is None and y is None:
        x_coord = (window.SCREEN_WIDTH / 2) - (text_rect.width / 2)
        y_coord = (window.SCREEN_HEIGHT / 2) - (text_rect.height / 2)
    elif x is None:
        x_coord = (window.SCREEN_WIDTH / 2) - (text_rect.width / 2)
    elif y is None:
        y_coord = (window.SCREEN_HEIGHT / 2) - (text_rect.height / 2)

    if shadow:
        text_shadow = font.render(text, True, shadow['color'])
        text_shadow.set_alpha(shadow['opacity'])
        shadow_x = x_coord + shadow['x']
        shadow_y = y_coord + shadow['y']
        window.canvas.blit(text_shadow, [shadow_x, shadow_y])
    window.canvas.blit(text_render, [x_coord, y_coord])
