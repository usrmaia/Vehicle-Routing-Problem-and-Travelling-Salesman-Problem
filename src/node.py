class Node:
    def __init__(self, id: int, coord_x: float, coord_y: float):
        self.id = id
        self.coord_x = coord_x
        self.coord_y = coord_y
        self._distance_to = {}

    def distanceTo(self, node: "Node") -> float:
        # TODO testar salvando as distancias no dicionário e não salvando as distâncias mas calculando e retornando
        if self.id in node._distance_to:
            return node._distance_to[self.id]

        if node.id in self._distance_to:
            return self._distance_to[node.id]

        distance = self.euclideanDistance(node)
        self._distance_to[node.id] = distance

        return distance

    def euclideanDistance(self, node: "Node") -> float:
        return (
            (self.coord_x - node.coord_x) ** 2 + (self.coord_y - node.coord_y) ** 2
        ) ** 0.5

    def __str__(self) -> str:
        return f"({self.id}, {self.coord_x}, {self.coord_y})"

    def __eq__(self, node: "Node") -> bool:
        return self.coord_x == node.coord_x and self.coord_y == node.coord_y


if __name__ == "__main__":
    n1 = Node(1, 1, 1)
    n2 = Node(2, 2, 2)
    n3 = Node(3, 3, 3)

    print(n1.distanceTo(n2))
    print(n2.distanceTo(n1))
