from Window import Window
from window.window_utils import add_button, add_text
import pygame


###################################
# MAIN MENU #######################
###################################
def MENU_main(window: Window):
    add_button(
        window=window,
        text="PLAY",
        y=window.SCREEN_HEIGHT / 2 - 140,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.start_new_snake,
        func_params=None
    )
    add_button(
        window=window,
        text="COMPUTOR",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_MENU"
    )

    add_button(
        window=window,
        text="LEAVE",
        y=window.SCREEN_HEIGHT / 2 + 80,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.exit_window
    )


###################################
# GAME INTERFACE ##################
###################################
def GAME_interface(window: Window):
    draw_snake = window.snake.game_over is False
    value = window.create_snakeboard(window.snake.size, draw_snake)
    x_size, y_size, x_start, y_start = value
    if window.snake.is_running is False and window.snake.game_over is False:
        add_text(window, "Press any direction to start", y=120)
    elif window.snake.is_running is False and window.snake.game_over is True:
        pygame.draw.rect(
            window.canvas,
            window.theme['board2'],
            pygame.Rect(x_start, y_start, x_size, y_size)
        )
        add_text(window, "Game is over !", y=120)

        add_text(
            window,
            "Stats",
            y=window.SCREEN_HEIGHT / 2 - 88,
            font=window.fontButton,
            shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
            })
        window.display_game_info(y=window.SCREEN_HEIGHT / 2 - 20)
        add_button(
            window,
            "REPLAY",
            y=window.SCREEN_HEIGHT / 2 + 42,
            font=window.fontText,
            bg_default=window.theme['btn'],
            bg_hover=window.theme['btn-hover'],
            border_radius=16,
            func=window.start_new_snake,
            func_params=None
        )
    else:
        window.display_game_info(y=120)
    add_button(
        window=window,
        text="LEAVE",
        y=window.SCREEN_HEIGHT - 100,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.leave_game
    )


###################################
# MENU COMPUTOR ###################
###################################
def MENU_computor(window: Window):
    add_button(
        window=window,
        text="VISUALIZATION",
        y=window.SCREEN_HEIGHT / 2 - 140,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_VISUALIZATION_SETTINGS"
    )
    add_button(
        window=window,
        text="TRAINING",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_TRAINING_SETTINGS"
    )

    add_button(
        window=window,
        text="BACK",
        y=window.SCREEN_HEIGHT / 2 + 80,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="MAIN"
    )


###################################
# MENU COMPUTOR VISUALIZATION #####
###################################
def MENU_computor_visualization(window: Window):
    add_button(
        window=window,
        text="BACK",
        y=window.SCREEN_HEIGHT - 100,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_MENU"
    )
    pass


###################################
# MENU COMPUTOR TRAINING ##########
###################################
def MENU_computor_training(window: Window):
    pygame.draw.polygon(
        window.canvas,
        window.theme['btn'],
        [(100, 100), (130, 130), (70, 100)]
    )
    pygame.draw.polygon(
        window.canvas,
        "#FFFFFF",
        [(100, 100), (130, 130), (70, 100)],
        3
    )

    add_text(window, "Sessions", y=window.SCREEN_HEIGHT / 2)
    add_button(
        window=window,
        y=window.SCREEN_HEIGHT / 2 + 60,
        text="146",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=print,
        func_params="Session number",
        font=window.fontText,
        border_radius=16
    )

    add_button(
        window=window,
        text="BACK",
        y=window.SCREEN_HEIGHT - 100,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_MENU"
    )
    pass
