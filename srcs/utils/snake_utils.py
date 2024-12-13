def is_enough_space_around(
        board: list[list[str]],
        i: int,
        j: int,
        allowed: list[str],
        radius: int = 1
) -> bool:
    rad_end = radius + 1
    start_i = i - radius if i - radius >= 0 else 0
    end_i = i + rad_end if i + rad_end <= len(board) else len(board)

    start_j = j - radius if j - radius >= 0 else 0
    end_j = j + rad_end if j + rad_end <= len(board[i]) else len(board[i])

    for i in range(start_i, end_i):
        for j in range(start_j, end_j):
            if board[i][j] not in allowed:
                return False
    return True
