#!/bin/python3

from srcs.Agent import Agent
import srcs.utils.Colors as Colors
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="A reinforcement learning-based snake game where the "
        "agent learns to improve its performance."
    )

    parser.add_argument(
        '-sessions',
        type=int,
        default=1,
        help="Number of training sessions to execute. Defaults to 1."
    )

    parser.add_argument(
        '-board',
        type=int,
        default=10,
        help="Size of the square board (e.g., 10 for a 10x10 grid). "
        "Defaults to 10."
    )

    parser.add_argument(
        '-speed',
        type=float,
        default=0.1,
        help="Speed of the snake in seconds per step when "
        "visualization is enabled. Defaults to 0.1."
    )

    parser.add_argument(
        '-load',
        type=str,
        help="Path to a pre-trained model file to load "
        "for testing or further training."
    )

    parser.add_argument(
        '-save',
        nargs='?',
        const=True,
        default=False,
        help="Path to save the trained model after the "
        "session. The model will be stored in the specified file."
    )

    parser.add_argument(
        '-visual',
        type=str,
        choices=["on", "off"],
        help="Toggle visualization of the snake's actions and "
        "decision-making process ('on' or 'off')."
    )

    parser.add_argument(
        '-dontlearn',
        action='store_false',
        help="Run the game without training to evaluate the "
        "current model's performance."
    )

    parser.add_argument(
        '-step-by-step',
        action='store_true',
        help="Enable step-by-step mode, requiring the user "
        "to press 'Enter' to advance each step."
    )

    parser.add_argument(
        '-graph-only',
        action='store_true',
        help="Display only the training statistics of the "
        "model in a graph without running."
    )

    try:
        args = parser.parse_args()

        sessions_number = args.sessions
        board_size = args.board

        load_model = args.load
        save_model = args.save
        if args.visual == "on":
            visualization = True
        else:
            visualization = False
        learn = args.dontlearn
        if learn is False:
            epsilon = 0
        else:
            epsilon = 1
        stepbystep = args.step_by_step
        speed = args.speed

        agent = Agent(
            board_size=board_size,
            sessions_number=sessions_number,
            model_name=load_model,
            learn=learn
        )

        if args.graph_only is True:
            agent.visualization_history()
            return
        history = agent.run_agent(
            learning_rate=0.1,
            gamma=0.99,
            epsilon=epsilon,
            epsilon_decay=0.99,
            epsilon_min=0.01,
            visualization=visualization,
            speed=speed,
            step_by_step=stepbystep
        )
        if save_model is not False:
            if save_model is True:
                agent.save_model()
            else:
                agent.save_model(save_model)
        if sessions_number > 1:
            agent.visualization_history(history)

    except Exception as e:
        URED = Colors.URED
        BHRED = Colors.BHRED
        RESET = Colors.RESET
        RED = Colors.RED
        error_msg = f"{URED}{BHRED}Error{RESET}\n"
        error_msg += f"{BHRED}Name: {RED}{type(e).__name__}\n"
        error_msg += f"{BHRED}Message: {RED}{e}\n"
        print(error_msg)


if __name__ == "__main__":
    main()
