class WindowTheme:
    def __init__(self, THEME: str = "blue"):
        self.__theme = THEME
        self.__blue_range = {
            "bg1": "#1D1B62",
            "bg2": "#222169",
            "board1": "#2E2E4D",
            "board2": "#222241",
        }
        pass

    def get(self):
        if self.__theme == "blue":
            return self.__blue_range
