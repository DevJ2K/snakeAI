from srcs.SnakeNode import SnakeNode
from utils.Colors import *

class SnakeError(Exception):
    pass


class Snake:
    def __init__(self, size: int = 10, snake_length: int = 3) -> None:
        if size < 10 or size % 5 != 0:
            raise SnakeError("The board size must be greater than "
                             "or equal to 10 and divisible by 5.")
        if snake_length < 1 or 3 < snake_length:
            raise SnakeError("The snake length must be greater than "
                             "or equal to 1.")

        self.WALL = {'char': 'W', 'color': BLACKHB}
        self.HEAD = {'char': 'H', 'color': CYANHB}
        self.SNAKE_BODY = {'char': 'S', 'color': BLUEHB}
        self.GREEN_APPLE = {'char': 'G', 'color': GREENHB}
        self.RED_APPLE = {'char': 'R', 'color': REDHB}
        self.EMPTY_SPACE = {'char': '0', 'color': BLACKB}

        self.all_items = [
            self.WALL,
            self.HEAD,
            self.SNAKE_BODY,
            self.GREEN_APPLE,
            self.RED_APPLE,
            self.EMPTY_SPACE
        ]

        self.size = size

        self.board: list[list[str]] = self.__create_board()
        self.snake: list[SnakeNode] = []

    def __create_board(self) -> list[list[str]]:
        board = [[self.EMPTY_SPACE['char'] for _ in range(self.size)] for __ in range(self.size)]
        for line in board:
            line.insert(0, self.WALL['char'])
            line.append(self.WALL['char'])
        board.insert(0, [self.WALL['char'] for _ in range(self.size + 2)])
        board.append([self.WALL['char'] for _ in range(self.size + 2)])
        return board

    def place_snake(self):
        pass


    def get_item_by_char(self, char: str) -> dict | None:
        for item in self.all_items:
            if item['char'] == char:
                return item
        return None

    def display_board(self, spacing: bool = False):
        display_str = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                item = self.get_item_by_char(self.board[i][j])
                if item is not None:
                    display_str += item['color'] + "  " + RESET
                    if spacing:
                        display_str += " "
            display_str += "\n"
            if spacing:
                display_str += "\n"
        print(display_str)

if __name__ == "__main__":
    from pprint import pprint
    snake = Snake(size=10, snake_length=3)
    # snake.display_board(False)
    pprint(snake.board)

    pass
