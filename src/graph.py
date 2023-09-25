from node import Node


class Graph:
    def __init__(self):
        self._distance_to = {}

    def distanceTo(self, node1: Node, node2: Node) -> float:
        if node1.id in self._distance_to:
            if node2.id in self._distance_to[node1.id]:
                return self._distance_to[node1.id][node2.id]
        elif node2.id in self._distance_to:
            if node1.id in self._distance_to[node2.id]:
                return self._distance_to[node2.id][node1.id]

        distance = self.euclideanDistance(node1, node2)

        if node1.id not in self._distance_to:
            self._distance_to[node1.id] = {}
        self._distance_to[node1.id][node2.id] = distance

        return distance

    def euclideanDistance(self, node1: Node, node2: Node) -> float:
        return (
            (node1.coord_x - node2.coord_x) ** 2 + (node1.coord_y - node2.coord_y) ** 2
        ) ** 0.5
