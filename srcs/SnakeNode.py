class SnakeNode:
    def __init__(
            self,
            pos: tuple[int, int],
            direction: tuple[int, int],
            head: bool = False
    ) -> None:
        self.i = pos[0]
        self.j = pos[1]

        self.head = head
        self.direction = direction
        self.opposite_direction = None
        # self.next_node = None
        # self.previous_node = None

    def apply_direction(self, direction: tuple[int, int]):
        self.i += direction[0]
        self.j += direction[1]

    def new_coordinate(self, i: int, j: int):
        self.i = i
        self.j = j
