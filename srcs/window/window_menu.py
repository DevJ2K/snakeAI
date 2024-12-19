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
        func=window.run_settings_vision
    )
    add_button(
        window=window,
        text="TRAINING",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.run_settings_training
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
        text=str(window.agent.size),
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
        func_params=10,
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
        func_params=30,
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
        text=window.agent.get_model_name(20),
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
        func=window.run_computor_visualization,
        func_params="MODEL_VISUALIZATION"
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


###################################
# MENU COMPUTOR TRAINING ##########
###################################
def MENU_computor_training(window: Window):
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
        text=str(window.agent.size),
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
        func_params=10,
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
        func_params=20,
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
        text=window.agent.get_model_name(20),
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.select_model,
        font=window.fontText,
        border_radius=24
    )

    add_button(
        window=window,
        text="TRAIN",
        x=window.SCREEN_WIDTH / 2 + 40,
        y=window.SCREEN_HEIGHT - 100,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.run_computor_visualization,
        func_params="TRAINING_VISUALIZATION"
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


###################################
# COMPUTOR VISUALIZATION ##########
###################################
def RUN_training_visualization(window: Window):
    # draw_snake = window.snake.game_over is False
    value = window.create_snakeboard(window.snake.size, True)
    agent = window.agent

    font_text = window.get_font(size=36)
    font_subtext = window.get_font(size=30)

    # add_text(window, "Press 'left' or 'right' arrow to "
    #          f"increase the speed. ({window.speed})",
    #          y=120)

    add_text(
        window,
        "Sessions",
        x=120,
        y=window.SCREEN_HEIGHT / 2 - 140,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )
    add_text(
        window,
        f"{agent.w_session}/{agent.sessions_number}",
        x=120,
        y=window.SCREEN_HEIGHT / 2 - 100,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_subtext
    )

    add_text(
        window,
        "Duration",
        x=120,
        y=window.SCREEN_HEIGHT / 2 - 10,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )
    add_text(
        window,
        "6m14s",
        x=120,
        y=window.SCREEN_HEIGHT / 2 + 30,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_subtext
    )
    add_text(
        window,
        "Best Session",
        x=window.SCREEN_WIDTH - 300,
        y=window.SCREEN_HEIGHT / 2 - 140,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )


    add_text(
        window,
        "Current Session",
        x=window.SCREEN_WIDTH - 300,
        y=window.SCREEN_HEIGHT / 2 - 10,
        shadow={
                "color": window.theme['accent'],
                "opacity": 42,
                "x": 4,
                "y": 4,
        },
        font=font_text
    )
    window.display_current_session(font_subtext)
    window.display_best_session(font_subtext)

    if window.computor_vision:
        color = {
            'bg_default': '#00AA00',
            'bg_hover': '#007700'
        }
    else:
        color = {
            'bg_default': '#CC0000',
            'bg_hover': '#990000'
        }

    add_button(
            window=window,
            text="AGENT VISION",
            y=window.SCREEN_HEIGHT - 220,
            bg_default=color['bg_default'],
            bg_hover=color['bg_hover'],
            func=window.toggle_computor_vision,
            font=font_subtext,
            border_radius=16
        )

    add_button(
            window=window,
            text="END TRAINING",
            y=window.SCREEN_HEIGHT - 100,
            bg_default=window.theme['btn'],
            bg_hover=window.theme['btn-hover'],
            func=window.leave_game
        )


def RUN_model_visualization(window: Window):

    add_button(
            window=window,
            text="END SESSION",
            y=window.SCREEN_HEIGHT - 100,
            bg_default=window.theme['btn'],
            bg_hover=window.theme['btn-hover'],
            func=window.leave_game
        )
