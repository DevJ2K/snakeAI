import pytest
from srcs.Snake import Snake, SnakeError
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_snake_instanciation():
    Snake(size=10, snake_length=3)
    Snake(size=15, snake_length=3)
    Snake(size=20, snake_length=3)


def test_snake_invalid_board_size():
    sizes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 16]
    for size in sizes:
        with pytest.raises(SnakeError):
            Snake(size=size, snake_length=5)


def test_snake_invalid_snake_length():
    lengths = [0, 4, 5, 6, 7, 8, 9]
    for length in lengths:
        with pytest.raises(SnakeError):
            Snake(size=15, snake_length=length)
