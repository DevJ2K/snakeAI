import os
import random
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
            model_name: str = None,
            learn: bool = True,
            output_file: str = None
            ) -> None:
        super().__init__(board_size)
        self.output_file = output_file
        self.sessions_number = sessions_number
        self.update_model = learn
        self.model = self.get_model(model_name)
        self.learn = learn

    def __str__(self) -> str:
        return str(self.model)

    def vision(self) -> list[list[str]]:
        head_i = self.snake[0].i
        head_j = self.snake[0].j
        vision_board = [
            ["*" for _ in range(len(self.board))]
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
        v_board = self.vision()  # Vision board
        g_board = self.board  # Game board

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

    #####################################
    # MODELS
    def get_model(self, file: str = None) -> dict:
        if file:
            file_parent_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(file_parent_dir)
            model_dir = os.path.join(root_dir, "models")
            model_file = os.path.join(model_dir, file)
            with open(model_file) as fd:
                return json.load(fd)
                # print(self.model)
        else:
            return {
                "session": 0,
                "max_length": 0,
                "max_movements": 0,
                "q_table": {}
            }

    def save_model(self, filename: str = None):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(root_dir, "models")
        if filename:
            file = os.path.join(model_dir, filename)
        else:
            i = 0
            while True:
                name = ""
                if i == 0:
                    name = f"{self.model['session']}sess.json"
                else:
                    name = f"{self.model['session']}sess({i}).json"
                file = os.path.join(model_dir, name)
                if os.path.exists(file):
                    i += 1
                else:
                    break
        try:
            with open(file, "w") as f:
                json.dump(self.model, f, indent=4)
        except Exception as e:
            print(f"Error: {e}")
        print(file)

    def display_stats(self):
        RESET = Colors.RESET
        BHCYAN = Colors.BHCYAN
        BHGREEN = Colors.BHGREEN
        BHYELLOW = Colors.BHYELLOW
        print(f"{BHGREEN}==== Model Stats ===={RESET}")
        print(Colors.BHWHITE, end="")
        print(f"Session(s): {BHCYAN}{self.model['session']}", RESET)
        print(Colors.BHWHITE, end="")
        print(f"Max length: {BHGREEN}{self.model['max_length']}", RESET)
        print(Colors.BHWHITE, end="")
        print(f"Max movements: {BHYELLOW}{self.model['max_movements']}", RESET)

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

    def __get_near_value(self, line: str) -> str:
        if len(line) == 0:
            return "*"
        else:
            wall_pos = line.find(self.WALL['char'])
            if wall_pos == 0:
                return self.WALL['char']

            ga_pos = line.find(self.GREEN_APPLE['char'])
            ra_pos = line.find(self.RED_APPLE['char'])
            body_pos = line.find(self.SNAKE_BODY['char'])
            empty_pos = line.find(self.EMPTY_SPACE['char'])
            pos_list = [ga_pos, ra_pos, body_pos]
            pos_list = [pos for pos in [ga_pos, ra_pos, body_pos] if pos != -1]

            if len(pos_list) == 0:
                return self.EMPTY_SPACE['char']
            else:
                if min(pos_list) == body_pos:
                    if empty_pos != -1 and empty_pos < body_pos:
                        return line[empty_pos]
                    else:
                        return line[body_pos]

                else:
                    return line[min(pos_list)]

    def board_state(self) -> str:
        head_i = self.snake[0].i
        head_j = self.snake[0].j
        up_line = agent_utils.get_up_line(self.board, head_i, head_j)
        up_line = up_line[::-1]
        down_line = agent_utils.get_down_line(self.board, head_i, head_j)
        left_line = agent_utils.get_left_line(self.board, head_i, head_j)
        left_line = left_line[::-1]
        right_line = agent_utils.get_right_line(self.board, head_i, head_j)

        # GA_UP|GA_DOWN|GA_LEFT|GA_RIGHT|OBS_NEAR_UP|...|
        ga_char = self.GREEN_APPLE['char']
        state = ""
        state += "y" if up_line.find(ga_char) != -1 else "n"
        state += "y" if down_line.find(ga_char) != -1 else "n"
        state += "y" if left_line.find(ga_char) != -1 else "n"
        state += "y" if right_line.find(ga_char) != -1 else "n"

        state += self.__get_near_value(up_line)
        state += self.__get_near_value(down_line)
        state += self.__get_near_value(left_line)
        state += self.__get_near_value(right_line)

        return state

    def agent_next_frame(self, direction: tuple[int, int]) -> bool:
        next_i = self.snake[0].i + direction[0]
        next_j = self.snake[0].j + direction[1]
        apple = None

        if self.board[next_i][next_j] not in [
            self.GREEN_APPLE['char'],
            self.RED_APPLE['char'],
            self.EMPTY_SPACE['char'],
        ]:
            # return_value = False
            return False

        if self.board[next_i][next_j] == self.GREEN_APPLE['char']:
            apple = self.GREEN_APPLE
            self.snake.append(self._new_snake_node())
            self.green_apple_eat += 1
            self.snake_length += 1
            if self.snake_length > self.max_snake_length:
                self.max_snake_length = self.snake_length
        elif self.board[next_i][next_j] == self.RED_APPLE['char']:
            if self.snake_length == 1:
                self.snake_length -= 1
                return False
            apple = self.RED_APPLE
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

    def make_action(self, action: tuple[int]) -> tuple[str, int, bool]:
        head_i = self.snake[0].i
        head_j = self.snake[0].j

        new_pos_i = head_i + action[0]
        new_pos_j = head_j + action[1]

        reward = -1
        is_game_over = False
        if self.board[new_pos_i][new_pos_j] == self.GREEN_APPLE['char']:
            reward = 10
        elif self.board[new_pos_i][new_pos_j] == self.RED_APPLE['char']:
            reward = -10
        if self.next_frame(action) is False:
            reward = -30
            is_game_over = True
        state = self.board_state()
        # for i in range(4):
        #     if state[i] == "y" and state[4 + i] == "G":
        #         reward += 2

        return state, reward, is_game_over

    def __get_max_value(self, state, action: tuple[int]):
        return max(self.model["q_table"][state])
        opposite_direction = (-action[0], -action[1])
        forbidden_action = self.directions.index(opposite_direction)
        old_forbidden = self.model["q_table"][state][forbidden_action]
        self.model["q_table"][state][forbidden_action] = float("-inf")
        max_value = max(self.model["q_table"][state])
        self.model["q_table"][state][forbidden_action] = old_forbidden
        return max_value

    def __get_actions(
            self, exclude_directions: list[tuple[int]]) -> list[tuple[int]]:
        valid_directions = []
        for direction in self.directions:
            if direction not in exclude_directions:
                valid_directions.append(direction)
        if len(valid_directions) == 0:
            return self.directions
        else:
            return valid_directions

    def __get_exploitable_action(
            self, state, allowed_actions: list[tuple[int]]) -> tuple[int]:
        allowed_indexes = []
        for i, direction in zip(range(len(self.directions)), self.directions):
            if direction in allowed_actions:
                allowed_indexes.append(i)

        state_tab = self.model["q_table"][state]
        tmp_list = []
        for i, state in zip(range(len(state_tab)), state_tab):
            if i in allowed_indexes:
                tmp_list.append(state)
            else:
                tmp_list.append(float("-inf"))

        max_value = max(tmp_list)
        pos = tmp_list.index(max_value)
        return self.directions[pos]

        # if len(allowed_indexes) == len(self.directions):
        #     return random.choice(self.directions)

        # forbidden_index = self.directions.index(opposite_direction)
        # old_forbidden = self.model["q_table"][state][forbidden_index]
        # # print(old_forbidden, forbidden_index)
        # self.model["q_table"][state][forbidden_index] = less_inf
        # max_value = max(self.model["q_table"][state])
        # action_index = self.model["q_table"][state].index(max_value)
        # action = self.directions[action_index]
        # self.model["q_table"][state][forbidden_index] = old_forbidden
        # pass
    def run_agent(
            self,
            learning_rate: float = 0.1,
            gamma: float = 0.99,  # Weight of next state
            epsilon: float = 1.0,
            epsilon_decay: float = 0.995,
            epsilon_min: float = 0.01
            ):
        for session in range(self.sessions_number):
            self.model["session"] += 1

            # INIT GAME
            self.new_game()
            movement = 0
            total_reward = 0

            while True and (self.learn is False or movement < 500):
                state = self.board_state()
                if self.model["q_table"].get(state) is None:
                    self.model["q_table"][state] = [0, 0, 0, 0]

                if self.learn is False:
                    self.display_board_and_vision()
                    time.sleep(0.3)

                head = self.snake[0]
                direction = head.direction
                opposite_direction = (-direction[0], -direction[1])
                exclude_direction = []
                for i in range(4):
                    if False:
                        # if state[4 + i] == self.WALL['char']
                        # elif state[4 + i] == self.SNAKE_BODY['char']:
                        exclude_direction.append(self.directions[i])
                if opposite_direction not in exclude_direction:
                    exclude_direction.append(opposite_direction)
                actions = self.__get_actions(exclude_direction)
                # print(state, actions)
                if random.uniform(0, 1) < epsilon:
                    # EXPLORATION | Choose a random action
                    action = random.choice(actions)
                    # action = None
                    # for i in range(4):
                    #     if state[i] == "y" and state[4 + i] == "G":
                    #         action = self.directions[i]
                    #         break
                else:
                    # EXPLOITATION | Best action of the action in q_table
                    action = self.__get_exploitable_action(state, actions)
                    # if max_value == 0:
                    #     for i in range(4):
                    #         if state[i] == "y" or state[4 + i] == "G":
                    #             action = self.directions[i]

                next_state, reward, is_game_over = self.make_action(action)

                index_action = self.directions.index(action)

                # Update q_table with Q_function
                if self.learn:
                    old_value = self.model["q_table"][state][index_action]
                    if self.model["q_table"].get(next_state) is None:
                        self.model["q_table"][next_state] = [0, 0, 0, 0]
                    next_max_value = self.__get_max_value(next_state, action)
                    next_max_value = max(self.model["q_table"][next_state])

                    cur_value = (1 - learning_rate) * old_value
                    bellman_equation = (reward + gamma * next_max_value)

                    new_value = cur_value + learning_rate * bellman_equation
                    self.model["q_table"][state][index_action] = new_value

                total_reward += reward
                movement += 1
                if is_game_over:
                    break

            new_max_movement = max(self.model['max_movements'], movement)
            self.model['max_movements'] = new_max_movement
            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

            print(f"Session n°{session + 1}, ", end="")
            print(f"Total Reward: {total_reward}, ", end="")
            print(f"Duration: {movement}, ", end="")
            print(f"Max len: {self.snake_length}")

        self.model["max_length"] = self.max_snake_length
        self.display_stats()


if __name__ == "__main__":
    # from pprint import pprint
    # from MeasureTime import MeasureTime

    # agent = Agent(model_file="models/10sess.json")
    MAIN = 0

    if MAIN == 0:  # TRAINING
        agent = Agent(model_name=None, sessions_number=1000, learn=True)
        # agent.display_board_and_vision()
        agent.run_agent(epsilon=1, epsilon_decay=0.995, epsilon_min=0.01)
        agent.save_model("tmp.json")
        # agent.display_stats()

    elif MAIN == 1:  # USE MODEL
        agent = Agent(
            board_size=20,
            model_name="10000sess(1).json",
            sessions_number=1,
            learn=False
        )
        # agent = Agent(sessions_number=1, learn=False)
        # print(agent.board_state())
        agent.display_board_and_vision()
        agent.run_agent(epsilon=0, epsilon_decay=0.995, epsilon_min=0.01)
    # mt.stop()
    # agent.save_model()
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
    # print(f"GAMEOVER: {agent.green_apple_eat} GA | {agent.red_apple_eat} RA")
