import os
import sys
from srcs.Agent import Agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_open_model_wrong_args():
    model = {
        "session": 0,
        "max_length": 0,
        "max_movements": 0,
        "q_table": {}
    }
    files = [
        "invalid_models/no_args.json",
        "invalid_models/wrong_session.json",
        "invalid_models/wrong_max_len.json",
        "invalid_models/wrong_q_table.json",
    ]
    for file in files:
        assert Agent(model_name=file).model == model
