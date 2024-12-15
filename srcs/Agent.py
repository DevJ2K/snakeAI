import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srcs.Snake import Snake

class Agent(Snake):
    def __init__(self, size: int = 10, snake_length: int = 3) -> None:
        super().__init__(size, snake_length)
        pass


if __name__ == "__main__":
    agent = Agent()
    # agent.

if __name__ == "__main__":
    # from pprint import pprint

    agent = Agent(size=10, snake_length=3)
    # snake._Snake__place_random_apple({})
    agent.display_board(False)
    # time.sleep(2)
    direction_list = {
        "U": agent.UP,
        "D": agent.DOWN,
        "L": agent.LEFT,
        "R": agent.RIGHT
    }
    while True:
        next_direction = input("Direction -> ")
        if agent.next_frame(direction_list[next_direction.upper()]) is False:
            break
        agent.display_board(False)
    print(f"GAME OVER : {agent.green_apple_eat} GA | {agent.red_apple_eat} RA")
