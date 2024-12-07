from srcs.SnakeNode import SnakeNode
from utils.Colors import *
import random

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
        self.HEAD = {'char': 'H', 'color': CYANB}
        self.SNAKE_BODY = {'char': 'S', 'color': BLUEB}
        self.GREEN_APPLE = {'char': 'G', 'color': GREENHB}
        self.RED_APPLE = {'char': 'R', 'color': REDHB}
        self.EMPTY_SPACE = {'char': '0', 'color': BLACKB}

        self.UP = (-1, 0)
        self.DOWN = (1, 0)
        self.LEFT = (0, -1)
        self.RIGHT = (0, 1)

        self.directions = [
            self.UP,
            self.DOWN,
            self.LEFT,
            self.RIGHT,
        ]

        self.all_items = [
            self.WALL,
            self.HEAD,
            self.SNAKE_BODY,
            self.GREEN_APPLE,
            self.RED_APPLE,
            self.EMPTY_SPACE
        ]

        self.size = size
        self.snake_length = snake_length

        self.board: list[list[str]] = self.__create_board()
        self.snake: list[SnakeNode] = []
        self.__init_snake()

        self.__place_snake()

        # self.direction = None


    def __create_board(self) -> list[list[str]]:
        board = [[self.EMPTY_SPACE['char'] for _ in range(self.size)] for __ in range(self.size)]
        for line in board:
            line.insert(0, self.WALL['char'])
            line.append(self.WALL['char'])
        board.insert(0, [self.WALL['char'] for _ in range(self.size + 2)])
        board.append([self.WALL['char'] for _ in range(self.size + 2)])
        return board

    def __init_snake(self):
        random_i = random.randint(self.snake_length, self.size - (self.snake_length - 1))
        random_j = random.randint(self.snake_length, self.size - (self.snake_length - 1))

        self.snake.append(SnakeNode((random_i, random_j), random.choice(self.directions), True))

        for _ in range(1, self.snake_length):
            self.snake.append(self.__new_snake_node())

    def __place_snake(self):
        for node in self.snake:
            if node.head:
                self.board[node.i][node.j] = self.HEAD['char']
            else:
                self.board[node.i][node.j] = self.SNAKE_BODY['char']

    def __place_random_apple(self):
        possibility_slot = []
        pass

    def __new_snake_node(self) -> None:
        if len(self.snake) == 0:
            return
        last_node = self.snake[-1]

        reverse_pos = (-last_node.direction[0], -last_node.direction[1])
        print(reverse_pos)
        # reverse_pos[0] = -reverse_pos[0]
        # reverse_pos[1] = -reverse_pos[1]

        return SnakeNode(
            (last_node.i + reverse_pos[0], last_node.j + reverse_pos[1]),
            last_node.direction,
            False
        )

    def update_snake_nodes(self):
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
    snake.display_board(False)

    pass
