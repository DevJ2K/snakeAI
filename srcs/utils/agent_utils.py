def get_up_line(board: list[list[str]], head_i: int, head_j: int):
	line = ""
	for i in range(head_i):
		line += board[i][head_j]
	return line

def get_down_line(board: list[list[str]], head_i: int, head_j: int):
	line = ""
	for i in range(head_i + 1, len(board)):
		line += board[i][head_j]
	return line

def get_left_line(board: list[list[str]], head_i: int, head_j: int):
	line = ""
	for j in range(head_j):
		line += board[head_i][j]
	return line

def get_right_line(board: list[list[str]], head_i: int, head_j: int):
	line = ""
	for j in range(head_j + 1, len(board[head_i])):
		line += board[head_i][j]
	return line
