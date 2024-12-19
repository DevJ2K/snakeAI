#!/bin/python3

from srcs.Agent import Agent
import srcs.utils.Colors as Colors
import argparse


def main():
    parser = argparse.ArgumentParser(description="A snake able to learns with reinforcement learning.")

    parser.add_argument(
        '-sessions',
        type=int,
        default=1,
        help="The numbers of sessions will do for training."
    )

    parser.add_argument(
        '-board',
        type=int,
        default=10,
        help="The size of the board."
    )

    parser.add_argument(
        '-speed',
        type=float,
        default=0.1,
        help="The speed of the snake when visualization is true."
    )

    parser.add_argument(
        '-load',
        type=str,
        help="Load a model from the given file."
    )

    parser.add_argument(
        '-save',
        type=str,
        help="Save the training session of the model in a file (stored in model directory)."
    )

    parser.add_argument(
        '-visual',
        type=str,
        choices=["on", "off"],
        help="To display the snake vision and action through time."
    )
    parser.add_argument(
        '-dontlearn',
        action='store_false',
        help="To test the performance of the model."
    )
    parser.add_argument(
        '-step-by-step',
        action='store_true',
        help="If enabled, you will need to press 'enter' to view the next choice."
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
        stepbystep = args.step_by_step
        speed = args.speed

        agent = Agent(
            board_size=board_size,
            sessions_number=sessions_number,
            model_name=load_model,
            learn=learn
        )
        history = agent.run_agent(
            learning_rate=0.1,
            gamma=0.99,
            epsilon=1,
            epsilon_decay=0.995,
            epsilon_min=0.01,
            visualization=visualization,
            speed=speed,
            step_by_step=stepbystep
        )
        if save_model is not None:
            agent.save_model(save_model)
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
