import os
import random
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from srcs.Snake import Snake
import srcs.utils.Colors as Colors
import srcs.utils.agent_utils as agent_utils
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
        self.display_stats()
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
        model = {
            "session": 0,
            "max_length": 0,
            "max_movements": 0,
            "history": [],
            "q_table": {}
        }
        if file:
            # file_parent_dir = os.path.dirname(os.path.abspath(__file__))
            # root_dir = os.path.dirname(file_parent_dir)
            # model_dir = os.path.join(root_dir, "models")
            # model_file = os.path.join(model_dir, file)
            file = os.path.abspath(file)
            try:
                with open(file) as fd:
                    model = json.load(fd)
                BHGREEN = Colors.BHGREEN
                RESET = Colors.RESET
                print(f"{BHGREEN}Model has been recovered: {RESET}", end="")
                print(f"{Colors.BHWHITE}{file}{RESET}")
            except Exception as e:
                print(Colors.BHRED, end="")
                print(f"Failed to load the model: {file}", end="")
                print(Colors.RESET)
                print(f"{Colors.RED}{e}{Colors.RESET}")

        print(Colors.BRED, end="")
        value = model.get("session")
        if value is None or not isinstance(value, int):
            print(f"'session' is not found or not an integer. ({value})")
            model['session'] = 0

        value = model.get("max_length")
        if value is None or not isinstance(value, int):
            print(f"'max_length' is not found or not an integer. ({value})")
            model['max_length'] = 0

        value = model.get("max_movements")
        if value is None or not isinstance(value, int):
            print(f"'max_movements' is not found or not an integer. ({value})")
            model['max_movements'] = 0

        value = model.get("history")
        if value is None or not isinstance(value, int):
            print(f"'history' is not found or not an array. ({value})")
            model['history'] = []

        value = model.get("q_table")
        if value is None or not isinstance(value, dict):
            print(f"'q_table' is not found or not a dictionnary. ({value})")
            model['q_table'] = {}
        print(Colors.RESET, end="")
        return model

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
            BHGREEN = Colors.BHGREEN
            RESET = Colors.RESET
            print(f"{BHGREEN}Model has been saved in: {RESET}", end="")
            print(f"{Colors.BHWHITE}{file}{RESET}")
        except Exception as e:
            print(Colors.BHRED, end="")
            print(f"Failed to save the model in: {file}", end="")
            print(Colors.RESET)
            print(f"{Colors.RED}{e}{Colors.RESET}")

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

    def visualization_history(self):
        pass

    def display_training_session_result(
            self,
            total_rewards,
            movements
            ):
        RESET = Colors.RESET
        BHCYAN = Colors.BHCYAN
        BHGREEN = Colors.BHGREEN
        BHYELLOW = Colors.BHYELLOW
        BHMAG = Colors.BHMAG
        print(f"{BHGREEN}==== Session Stats ===={RESET}")
        print(Colors.BHWHITE, end="")
        print(f"Total Rewards: {BHCYAN}{total_rewards}", RESET)
        print(Colors.BHWHITE, end="")
        print(f"Green Apple: {BHGREEN}{self.green_apple_eat}", RESET)
        print(Colors.BHWHITE, end="")
        print(f"Red Apple: {BHGREEN}{self.red_apple_eat}", RESET)
        print(Colors.BHWHITE, end="")
        print(f"Max length: {BHMAG}{self.max_snake_length}", RESET)
        print(Colors.BHWHITE, end="")
        print(f"Movements: {BHYELLOW}{movements}", RESET)

    #####################################
    # REINFORCEMENT LEARNING

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

    def make_action(self, action: tuple[int]) -> tuple[str, int, bool]:
        head_i = self.snake[0].i
        head_j = self.snake[0].j

        new_pos_i = head_i + action[0]
        new_pos_j = head_j + action[1]

        reward = -1
        is_game_over = False
        if self.board[new_pos_i][new_pos_j] == self.GREEN_APPLE['char']:
            reward = 15
        elif self.board[new_pos_i][new_pos_j] == self.RED_APPLE['char']:
            reward = -10
        if self.next_frame(action) is False:
            reward = -50
            is_game_over = True
        state = self.board_state()

        return state, reward, is_game_over

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

    def __display_session_vision(
            self,
            state,
            previous_action,
            type_action,
            previous_reward,
            waiting_time: float = 0.8
    ):
        if previous_action == "":
            return
        os.system('clear')
        if type_action == "EXPLORATION":
            print(f"{Colors.BHCYAN}{type_action}{Colors.RESET}", end="")
        else:
            print(f"{Colors.BHMAG}{type_action}{Colors.RESET}", end="")

        print(Colors.BHWHITE, end=" | State: ")
        print(f"{Colors.BHYELLOW}{state}", end="")

        print(Colors.BHWHITE, end=" | Reward: ")
        if previous_reward < 0:
            print(f"{Colors.BHRED}{previous_reward}", end="")
        else:
            print(f"{Colors.BHGREEN}{previous_reward}", end="")

        print(Colors.BHWHITE, end=" | Action: ")
        print(f"{previous_action}")
        print(Colors.RESET)
        self.display_board_and_vision()
        time.sleep(waiting_time)

    def run_agent(
            self,
            learning_rate: float = 0.1,
            gamma: float = 0.99,  # Weight of next state
            epsilon: float = 1.0,
            epsilon_decay: float = 0.995,
            epsilon_min: float = 0.01,
            speed: float = 0.3
            ):
        if self.sessions_number <= 0:
            return
        for session in range(self.sessions_number):
            self.model["session"] += 1

            # INIT GAME
            self.new_game()
            movement = 0
            total_reward = 0
            previous_action = ""
            previous_reward = 0
            previous_state = ""
            type_action = ""

            while True and (self.learn is False or movement < 500):
                state = self.board_state()
                is_new_state = self.model["q_table"].get(state) is None
                if is_new_state:
                    self.model["q_table"][state] = [0, 0, 0, 0]

                if self.learn is False:
                    self.__display_session_vision(
                        previous_state,
                        previous_action,
                        type_action,
                        previous_reward,
                        speed
                    )

                head = self.snake[0]
                direction = head.direction
                opposite_direction = (-direction[0], -direction[1])
                exclude_direction = [opposite_direction]
                actions = self.__get_actions(exclude_direction)

                if random.uniform(0, 1) < epsilon:
                    # EXPLORATION | Choose a random action
                    action = random.choice(actions)
                    type_action = "EXPLORATION"
                else:
                    # EXPLOITATION | Best action of the action in q_table
                    action = self.__get_exploitable_action(state, actions)
                    type_action = "EXPLOITATION"

                for i in range(len(self.directions)):
                    if self.directions[i] == action:
                        previous_action = self.direction_name[i]
                        break
                next_state, reward, is_game_over = self.make_action(action)
                previous_reward = reward
                previous_state = state

                index_action = self.directions.index(action)

                # Update q_table with Q_function
                if self.learn:
                    old_value = self.model["q_table"][state][index_action]
                    if self.model["q_table"].get(next_state) is None:
                        self.model["q_table"][next_state] = [0, 0, 0, 0]
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

            self.model['history'].append((
                self.snake_length,
                self.green_apple_eat,
                self.red_apple_eat,
                movement
            ))
            if self.learn is True:
                print(Colors.BHWHITE, end="")
                print(f"Session n°{session + 1}, ", end="")
                print(f"Total Reward: {total_reward}, ", end="")
                print(f"Duration: {movement}, ", end="")
                print(f"Max len: {self.snake_length}", end="")
                print(Colors.RESET)

        if self.learn is True:
            self.model["max_length"] = self.max_snake_length
            self.display_stats()
        else:
            self.__display_session_vision(
                previous_state,
                previous_action,
                type_action,
                previous_reward,
                speed
            )
            self.display_training_session_result(
                total_reward,
                movement
            )


if __name__ == "__main__":
    # from pprint import pprint
    # from MeasureTime import MeasureTime

    # agent = Agent(model_file="models/10sess.json")
    MAIN = 1

    if MAIN == 0:  # TRAINING
        agent = Agent(
            model_name=None,
            sessions_number=2500,
            learn=True)
        # agent.display_board_and_vision()
        agent.run_agent(
            epsilon=1,
            gamma=0.85,
            epsilon_decay=0.995,
            epsilon_min=0.01)
        agent.save_model("tmp.json")
        # agent.display_stats()

    elif MAIN == 1:  # USE MODEL
        agent = Agent(
            board_size=10,
            model_name="models/tmp.json",
            sessions_number=1,
            learn=False
        )
        # agent = Agent(sessions_number=1, learn=False)
        # print(agent.board_state())
        # agent.display_board_and_vision()
        agent.run_agent(
            epsilon=0,
            epsilon_decay=0.995,
            epsilon_min=0.01,
            speed=0.05)
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
