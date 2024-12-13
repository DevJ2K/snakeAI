# from Window import Window

def MENU_main(window):
    window.add_button(
        text="PLAY",
        y=window.SCREEN_HEIGHT / 2 - 140,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.start_new_snake,
        func_params=None
    )
    window.add_button(
        text="COMPUTOR",
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.switch_menu,
        func_params="COMPUTOR_MENU"
    )

    window.add_button(
        text="LEAVE",
        y=window.SCREEN_HEIGHT / 2 + 80,
        bg_default=window.theme['btn'],
        bg_hover=window.theme['btn-hover'],
        func=window.exit_window
    )
