from Window import Window
from window.window_utils import add_button, add_text, add_triangle_button
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
    # pygame.draw.polygon(
    #     window.canvas,
    #     window.theme['btn'],
    #     [(100, 100), (130, 130), (70, 100)]
    # )
    # pygame.draw.polygon(
    #     window.canvas,
    #     "#FFFFFF",
    #     [(100, 100), (130, 130), (70, 100)],
    #     3
    # )
    font_text = window.get_font(size=36)

    add_text(
        window,
        "BOARD SIZE",
        y=window.SCREEN_HEIGHT / 2 - 200,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )
    add_button(
        window=window,
        y=window.SCREEN_HEIGHT / 2 - 140,
        text=str(window.training.board_size),
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=None,
        func_params="Session number",
        font=window.fontText,
        border_radius=24
    )

    add_triangle_button(
        window=window,
        x=window.SCREEN_WIDTH / 2 - 60,
        y=window.SCREEN_HEIGHT / 2 - 106,
        base=40,
        height=40,
        direction="LEFT",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.decrease_board_size,
        func_params=None,
    )
    add_triangle_button(
        window=window,
        x=window.SCREEN_WIDTH / 2 + 60,
        y=window.SCREEN_HEIGHT / 2 - 106,
        base=40,
        height=40,
        direction="RIGHT",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.increase_board_size,
        func_params=None,
    )

    add_text(
        window,
        "SESSIONS",
        y=window.SCREEN_HEIGHT / 2 - 80,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )
    if window.is_editing_session_num:
        bg_default = window.theme['btn-hover']
    else:
        bg_default = window.theme['btn']
    add_button(
        window=window,
        y=window.SCREEN_HEIGHT / 2 - 20,
        text=window.session_num_display,
        bg_default=bg_default,
        bg_hover=window.theme['btn-hover'],
        func=window.edit_sessions_number,
        func_params=None,
        font=window.fontText,
        border_radius=24,
    )

    add_text(
        window,
        "LOAD MODEL",
        y=window.SCREEN_HEIGHT / 2 + 40,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )
    add_button(
        window=window,
        y=window.SCREEN_HEIGHT / 2 + 100,
        text=window.training.get_model_name(20),
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.select_model,
        font=window.fontText,
        border_radius=24
    )


    add_button(
        window=window,
        text="START",
        x=window.SCREEN_WIDTH / 2 + 40,
        y=window.SCREEN_HEIGHT - 100,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_MENU"
    )

    add_button(
        window=window,
        text="BACK",
        x=window.SCREEN_WIDTH / 2 - 160,
        y=window.SCREEN_HEIGHT - 100,
        bg_default="#d21b13",
        bg_hover="#9d0b04",
        func=window.switch_menu,
        func_params="COMPUTOR_MENU"
    )

