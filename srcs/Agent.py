import os
import sys
import random
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srcs.Snake import Snake
import utils.Colors as Colors
import utils.agent_utils as agent_utils
import json
import time

class Agent(Snake):
    def __init__(
            self,
            board_size: int = 10,
            sessions_number: int = 3,
            model_file: str = None,
            learn: bool = False,
            output_file: str = None
            ) -> None:
        super().__init__(board_size)
        self.model = self.get_model(model_file)
        self.output_file = output_file
        self.sessions_number = sessions_number
        self.update_model = learn

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
                "max_movements": 0,
                "q_table": {}
            }

    def save_model(self, output_file: str = None):
        if output_file:
            pass
        else:
            pass

    #####################################
    # REINFORCEMENT LEARNING
    def __prune_line(self, line: str) -> str:
        prune = False
        c_wall = self.WALL['char']
        c_empty = self.EMPTY_SPACE['char']
        tmp_list = [c_wall, c_empty]
        for char in line:
            if char not in tmp_list:
                prune = True
                break
        if prune is False:
            return line
        if line.startswith(c_wall):
            return line.lstrip(c_wall).lstrip(c_empty)
        return line.rstrip(c_wall).rstrip(c_empty)

    def board_state(self) -> str:
        head_i = self.snake[0].i
        head_j = self.snake[0].j
        up_line = agent_utils.get_up_line(self.board, head_i, head_j)
        down_line = agent_utils.get_down_line(self.board, head_i, head_j)
        left_line = agent_utils.get_left_line(self.board, head_i, head_j)
        right_line = agent_utils.get_right_line(self.board, head_i, head_j)

        prune_up = self.__prune_line(up_line)
        prune_down = self.__prune_line(down_line)
        prune_left = self.__prune_line(left_line)
        prune_right = self.__prune_line(right_line)
        # print("UP", up_line)
        # print("UP", prune_up)
        # print("DOWN", down_line)
        # print("DOWN", prune_down)
        # print("LEFT", left_line)
        # print("LEFT", prune_left)
        # print("RIGHT", right_line)
        # print("RIGHT", prune_right)

        return prune_up + prune_down + prune_left + prune_right

    def agent_next_frame(self, direction: tuple[int, int]) -> bool:
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
        return_value = True
        if self.board[next_i][next_j] not in [
            self.GREEN_APPLE['char'],
            self.RED_APPLE['char'],
            self.EMPTY_SPACE['char'],
        ]:
            return_value = False

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
                return_value = False
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
        return return_value

    def simulate_action(self, action: tuple[int]) -> tuple[str, int, bool]:
        head_i = self.snake[0].i
        head_j = self.snake[0].j

        new_pos_i = head_i + action[0]
        new_pos_j = head_j + action[1]

        reward = -10
        is_game_over = False
        if self.board[new_pos_i][new_pos_j] == self.GREEN_APPLE['char']:
            reward = 100
        elif self.board[new_pos_i][new_pos_j] == self.RED_APPLE['char']:
            reward = -100
        tmp_snake = copy.deepcopy(self)
        if tmp_snake.agent_next_frame(action) == False:
            reward = -300
            is_game_over = True
        state = tmp_snake.board_state()

        return state, reward, is_game_over


# alph a = 0. 1
# 5 gamma = 0.99
# 6 e p s i l o n = 1. 0
# 7 e p sil o n_ dec ay = 0.995
# 8 ep silon_min = 0.01
# 9 e p i s o d e s = 1000
# 10 max_steps = 1000
    def __get_max_value(self, state, action: tuple[int]):
        opposite_direction = (-action[0], -action[1])
        forbidden_action = self.directions.index(opposite_direction)
        old_forbidden = self.model["q_table"][state][forbidden_action]
        self.model["q_table"][state][forbidden_action] = float("-inf")
        max_value = max(self.model["q_table"][state])
        self.model["q_table"][state][forbidden_action] = old_forbidden
        return max_value


    def run_agent(
            self,
            learning_rate: float = 0.1,
            gamma: float = 0.99, # Weight of next state
            epsilon: float = 1.0,
            epsilon_decay: float = 0.995,
            epsilon_min: float = 0.01
            ):
        # for _ in range(self.sessions_number):
        # actions = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
        max_movement = 0
        for i in range(self.sessions_number):
            self.new_game()
            movement = 0
            total_reward = 0
            while True:
                state = self.board_state()
                # self.display_board_and_vision()
                # time.sleep(0.5)
                head = self.snake[0]
                direction = head.direction
                opposite_direction = (-direction[0], -direction[1])
                if self.model["q_table"].get(state) is None:
                    self.model["q_table"][state] = [0, 0, 0, 0]
                if random.uniform(0, 1) < epsilon:
                    # EXPLORATION
                    # Choose a random action
                    action = random.choice([elt for elt in self.directions if elt != opposite_direction])
                else:
                    # EXPLOITATION
                    # Take the best action of the action in q_table
                    forbidden_action = self.directions.index(opposite_direction)
                    old_forbidden = self.model["q_table"][state][forbidden_action]
                    self.model["q_table"][state][forbidden_action] = float("-inf")
                    max_value = max(self.model["q_table"][state])
                    max_action_index = self.model["q_table"][state].index(max_value)
                    action = self.directions[max_action_index]
                    self.model["q_table"][state][forbidden_action] = old_forbidden

                # next_state, reward, is_game_over = self.simulate_action(action)
                next_state, reward, is_game_over = "W00W0W", 0, random.randint(0, 10) == 5

                index_action = self.directions.index(action)
                old_value = self.model["q_table"][state][index_action]
                if self.model["q_table"].get(next_state) is None:
                    self.model["q_table"][next_state] = [0, 0, 0, 0]
                next_state_value = self.__get_max_value(next_state, action)

                # Update q_table with Q_function
                new_value = (1 - learning_rate) + old_value + learning_rate * (reward + gamma * next_state_value)

                self.model["q_table"][state][index_action] = new_value

                total_reward += reward
                self.next_frame(action)
                movement += 1
                if is_game_over:
                    break
                if opposite_direction == action:
                    raise Exception(f"WTF FRR {opposite_direction} | {action}")

            max_movement = max(max_movement, movement)
            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

            # print(f"Session n°{i}, Total Reward: {total_reward}, Duration: {duration}, Max len: {snake_len}")

        print(f"Max length: {self.max_snake_length}, Max movement: {max_movement}")


if __name__ == "__main__":
    from pprint import pprint
    from MeasureTime import MeasureTime

    # agent = Agent(model_file="models/10sess.json")
    agent = Agent(model_file=None, sessions_number=100)
    agent.display_board_and_vision()
    # print(agent.board_state())
    print(agent)
    # for i in range(10000):
    mt = MeasureTime(start=True)
    agent.run_agent(epsilon=1, epsilon_decay=0.995, epsilon_min=0.01)
    mt.stop()
    # print(agent)
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
