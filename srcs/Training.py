from pathlib import Path
import os


class Training:
    def __init__(
        self,
        board_size: int = 10,
        sessions_number: int = 1,
        model: str = None,
        learn: bool = False
    ) -> None:

        self.board_size: int = board_size
        self.sessions_number: int = sessions_number
        self.model: str = model
        self.learn: bool = learn

    def get_model_name(self, trunc: int = -1) -> str:
        if self.model is None:
            return "None"
        path = Path(self.model)
        filename = os.path.basename(path)
        if trunc == -1:
            return str(filename)
        trunc_word = str(filename)[0:trunc]
        if len(trunc_word) == len(filename):
            return str(filename)
        if len(trunc_word) == 0:
            return "None"
        if trunc_word[-1] == ".":
            return trunc_word + ".."
        return trunc_word + "..."

if __name__ == "__main__":
    training = Training(model="C:/Users/Théo/Desktop/refont_ludilab.zip")
    print(training.get_model_name(5))
