class Node:
    def __init__(self, id: int, coord_x: float, coord_y: float):
        self.id = id
        self.coord_x = coord_x
        self.coord_y = coord_y

    def __str__(self) -> str:
        return f"({self.id}, {self.coord_x}, {self.coord_y})"

    def __eq__(self, node: "Node") -> bool:
        return self.coord_x == node.coord_x and self.coord_y == node.coord_y


if __name__ == "__main__":
    n1 = Node(1, 1, 1)
    n2 = Node(2, 2, 2)
    n3 = Node(3, 3, 3)
