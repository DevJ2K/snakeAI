#!/bin/python3

import srcs.add_path as add_path
from srcs.Window import Window

if __name__ == "__main__":
    add_path.void()
    window = Window(title="SnakeAI", size=(1200, 900))
    window.launch()
