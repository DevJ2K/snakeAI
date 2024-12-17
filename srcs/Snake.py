from srcs.SnakeNode import SnakeNode
from utils.snake_utils import is_enough_space_around
import utils.Colors as Colors
import random
import time


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

        self.WALL = {
            'name': "WALL",
            'char': 'W',
            'color': Colors.BLACKHB,
            'hex': "#3A3A3A"
        }
        self.HEAD = {
            'name': "HEAD",
            'char': 'H',
            'color': Colors.MAGHB,
            'hex': "#16f4ff"
        }
        self.SNAKE_BODY = {
            'name': "SNAKE_BODY",
            'char': 'S',
            'color': Colors.BLUEB,
            'hex': "#16aaff"
        }
        self.GREEN_APPLE = {
            'name': "GREEN_APPLE",
            'char': 'G',
            'color': Colors.GREENHB,
            'hex': "#16ee3d"
        }
        self.RED_APPLE = {
            'name': "RED_APPLE",
            'char': 'R',
            'color': Colors.REDHB,
            'hex': "#ee2016"
        }
        self.EMPTY_SPACE = {
            'name': "EMPTY_SPACE",
            'char': '0',
            'color': Colors.BLACKB,
            'hex': "#AAAAAA"
        }

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
        self.default_length = snake_length
        self.max_snake_length = snake_length

        self.new_game()
        # self.direction = None

    def __create_board(self) -> list[list[str]]:
        board = [[self.EMPTY_SPACE['char']
                  for _ in range(self.size)] for __ in range(self.size)]
        for line in board:
            line.insert(0, self.WALL['char'])
            line.append(self.WALL['char'])
        board.insert(0, [self.WALL['char'] for _ in range(self.size + 2)])
        board.append([self.WALL['char'] for _ in range(self.size + 2)])
        return board

    def new_game(self):
        self.snake_length = self.default_length
        self.green_apple_eat = 0
        self.red_apple_eat = 0
        self.is_running = False
        self.game_over = False
        self.timer = None

        self.board: list[list[str]] = self.__create_board()
        self.snake: list[SnakeNode] = []
        self.__init_snake()

        self._place_snake()
        self.__place_apples()

    def get_board_with_border(self) -> list[list[str]]:
        return self.board

    def get_board_without_border(self) -> list[list[str]]:
        new_board: list[list[str]] = []
        for i in range(1, len(self.board) - 1):
            new_board.append([])
            for j in range(1, len(self.board[i]) - 1):
                new_board[i - 1].append(self.board[i][j])
        return new_board

    def __init_snake(self):
        a = self.snake_length
        b = self.size - (self.snake_length - 1)
        i = random.randint(a, b)
        j = random.randint(a, b)
        direction = random.choice(self.directions)

        self.snake.append(SnakeNode((i, j), direction, True))

        for _ in range(1, self.snake_length):
            self.snake.append(self._new_snake_node())

    def _place_snake(self):
        for node in self.snake:
            if node.head:
                self.board[node.i][node.j] = self.HEAD['char']
            else:
                self.board[node.i][node.j] = self.SNAKE_BODY['char']

    def _place_random_apple(self, apple: dict):
        possibility_slot = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if is_enough_space_around(
                    self.board, i, j, [
                        self.EMPTY_SPACE['char']
                    ], 0
                ):
                    possibility_slot.append((i, j))

        slot = random.choice(possibility_slot)
        self.board[slot[0]][slot[1]] = apple['char']
        # for possibility in possibility_slot:
        #     self.board[possibility[0]][possibility[1]] = "T"

    def __place_apples(self):
        possibility_slot = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if is_enough_space_around(
                    self.board, i, j, [
                        self.EMPTY_SPACE['char'],
                        self.GREEN_APPLE['char'],
                        self.RED_APPLE['char'],
                    ], 1
                ):
                    possibility_slot.append((i, j))

        # PLACE 2 GREEN APPLES
        for _ in range(2):
            slot = random.choice(possibility_slot)
            possibility_slot.remove(slot)
            self.board[slot[0]][slot[1]] = self.GREEN_APPLE['char']

        # PLACE 1 RED APPLE
        for _ in range(1):
            slot = random.choice(possibility_slot)
            possibility_slot.remove(slot)
            self.board[slot[0]][slot[1]] = self.RED_APPLE['char']

        # for possibility in possibility_slot:
        #     self.board[possibility[0]][possibility[1]] = "T"

    def _new_snake_node(self) -> None:
        if len(self.snake) == 0:
            return
        last_node = self.snake[-1]

        reverse_pos = (-last_node.direction[0], -last_node.direction[1])
        # reverse_pos[0] = -reverse_pos[0]
        # reverse_pos[1] = -reverse_pos[1]

        return SnakeNode(
            (last_node.i + reverse_pos[0], last_node.j + reverse_pos[1]),
            last_node.direction,
            False
        )

    # def get_snake_pos(self) -> tuple[int, int]:
    #     for i in range(len(self.board)):
    #         for j in range(len(self.board[i])):
    #             if self.board[i][j] == self.HEAD['char']:
    #                 return (i, j)

    def next_frame(self, direction: tuple[int, int]) -> bool:
        next_i = self.snake[0].i + direction[0]
        next_j = self.snake[0].j + direction[1]
        apple = None

        # self.all_items = [
        #     self.WALL,
        #     self.HEAD,
        #     self.SNAKE_BODY,
        #     self.GREEN_APPLE,
        #     self.RED_APPLE,
        #     self.EMPTY_SPACE
        # ]

        if self.board[next_i][next_j] not in [
            self.GREEN_APPLE['char'],
            self.RED_APPLE['char'],
            self.EMPTY_SPACE['char'],
        ]:
            return False

        if self.board[next_i][next_j] == self.GREEN_APPLE['char']:
            apple = self.GREEN_APPLE
            self.snake.append(self._new_snake_node())
            # print("GREENAPPLE", next_i, next_j)
            self.green_apple_eat += 1
            self.snake_length += 1
            if self.snake_length > self.max_snake_length:
                self.max_snake_length = self.snake_length
        elif self.board[next_i][next_j] == self.RED_APPLE['char']:
            if self.snake_length == 1:
                self.snake_length -= 1
                return False
            apple = self.RED_APPLE
            # print("REDAPPLE", next_i, next_j)
            pop_node = self.snake.pop()
            self.board[pop_node.i][pop_node.j] = self.EMPTY_SPACE['char']
            self.red_apple_eat += 1
            self.snake_length -= 1

        self.update_snake_nodes(direction, apple == self.GREEN_APPLE)
        self._place_snake()
        if apple is not None:
            self._place_random_apple(apple)
        # self.display_board()
        return True

    def update_snake_nodes(
            self,
            new_direction: tuple[int, int],
            new_node: bool = False
    ):
        if new_node is False:
            last_node = self.snake[-1]
            self.board[last_node.i][last_node.j] = self.EMPTY_SPACE['char']
        for i in range(len(self.snake) - 1, 0, -1):
            next_node = self.snake[i - 1]
            self.snake[i].new_coordinate(next_node.i, next_node.j)
        self.snake[0].apply_direction(new_direction)

    def get_item_by_char(self, char: str) -> dict | None:
        for item in self.all_items:
            if item['char'] == char:
                return item
        return None

    def get_item_by_coordinate(self, i: int, j: int) -> dict | None:
        return self.get_item_by_char(self.board[i][j])

    def display_board(self, spacing: bool = False):
        display_str = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                item = self.get_item_by_char(self.board[i][j])
                if item is not None:
                    display_str += item['color'] + "  " + Colors.RESET
                    if spacing:
                        display_str += " "
                else:
                    display_str += Colors.YELLOWHB + "  " + Colors.RESET
                    if spacing:
                        display_str += " "

            display_str += "\n"
            if spacing:
                display_str += "\n"
        print(display_str)

    def start_timer(self):
        self.timer = time.time()

    def end_timer(self):
        self.timer = time.time() - self.timer
        pass

    def get_timer(self):
        if self.is_running:
            return time.time() - self.timer
        return self.timer


if __name__ == "__main__":
    # from pprint import pprint

    snake = Snake(size=10, snake_length=3)
    # snake._Snake_place_random_apple({})
    snake.display_board(False)
    snake.new_game()
    # time.sleep(2)
    direction_list = {
        "U": snake.UP,
        "D": snake.DOWN,
        "L": snake.LEFT,
        "R": snake.RIGHT
    }
    while True:
        next_direction = input("Direction -> ")
        if snake.next_frame(direction_list[next_direction.upper()]) is False:
            break
        snake.display_board(False)
    print(f"GAME OVER : {snake.green_apple_eat} GA | {snake.red_apple_eat} RA")
