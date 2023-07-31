from .node import Node


class Route:
    def __init__(self):
        self._route: list[Node] = []
        self._cost: float = 0.0

    def setNode(self, node: Node, cost: float):
        self._route.append(node)
        self._cost += cost

    def setCost(self, cost: float):
        self._cost += cost

    def unsetCost(self, cost: float):
        self._cost -= cost

    def setNode(self, node: Node):
        self._route.append(node)

    def getCost(self):
        return self._cost

    def __str__(self) -> str:
        route = ""
        for position in range(len(self._route) - 1):
            route += str(self._route[position].id) + " -> "

        route += str(self._route[-1].id)
        return route

    def __lt__(self, route: "Route"):
        return self.getCost() < route.getCost()

    def getRoute(self) -> list[Node]:
        return self._route

    def __eq__(self, route: "Route") -> bool:
        return self._route == route.getRoute()

    def calculateTotalCost(self) -> float:
        self._cost = 0

        for position in range(len(self._route) - 1):
            self._cost += self._route[position].distanceTo(self._route[position + 1])

        self._cost += self._route[-1].distanceTo(self._route[0])

        return self._cost
