class SnakeNode:
    def __init__(self, pos: tuple[int, int], direction: tuple[int, int], head: bool = False) -> None:
        self.i = pos[0]
        self.j = pos[1]

        self.head = head
        self.direction = None
        self.next_node = None
        self.previous_node = None
