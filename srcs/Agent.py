import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srcs.Snake import Snake
import utils.Colors as Colors
import json

class Agent(Snake):
    def __init__(self, size: int = 10, snake_length: int = 3, model_file: str = None) -> None:
        super().__init__(size, snake_length)
        self.model = self.get_model(model_file)

    def __str__(self) -> str:
        return str(self.model)

    def vision(self) -> list[list[str]]:
        head_i = self.snake[0].i
        head_j = self.snake[0].j
        vision_board = [["*"
                for _ in range(len(self.board))]
                for __ in range(len(self.board[0]))
        ]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if head_i == i or head_j == j:
                    vision_board[i][j] = self.board[i][j]
        return vision_board

    def display_vision(self, spacing: bool = False):
        board = self.vision()
        display_str = ""
        for i in range(len(board)):
            for j in range(len(board[i])):
                item = self.get_item_by_char(board[i][j])
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

    def display_board_and_vision(self):
        v_board = self.vision() # Vision board
        g_board = self.board # Game board

        display_str = ""
        for i in range(len(g_board)):
            for j in range(len(g_board[i])):
                item = self.get_item_by_char(g_board[i][j])
                if item is not None:
                    display_str += item['color'] + "  " + Colors.RESET
                else:
                    display_str += Colors.YELLOWHB + "  " + Colors.RESET

            display_str += "  "
            for j in range(len(v_board[i])):
                item = self.get_item_by_char(v_board[i][j])
                if item is not None:
                    display_str += item['color'] + "  " + Colors.RESET
                else:
                    display_str += Colors.YELLOWHB + "  " + Colors.RESET

            display_str += "\n"
        print(display_str)

    def get_model(self, file: str = None) -> dict:
        if file:
            with open(file) as fd:
                return json.load(fd)
                # print(self.model)
        else:
           return {
                "session": 0,
                "max_sessions": 100,
                "max_length": 0,
                "max_duration": 0.0,
                "q_table": {}
            }



if __name__ == "__main__":
    # from pprint import pprint

    agent = Agent(size=10, snake_length=3, model_file="models/10sess.json")
    agent.display_board_and_vision()
    print(agent)
    # snake._Snake__place_random_apple({})
    # agent.display_board(False)
    # agent.display_vision(False)
    # time.sleep(2)
    # direction_list = {
    #     "U": agent.UP,
    #     "D": agent.DOWN,
    #     "L": agent.LEFT,
    #     "R": agent.RIGHT
    # }
    # while True:
    #     next_direction = input("Direction -> ")
    #     if agent.next_frame(direction_list[next_direction.upper()]) is False:
    #         break
    #     agent.display_board(False)
    # print(f"GAME OVER : {agent.green_apple_eat} GA | {agent.red_apple_eat} RA")
