from .node import Node


class Route:
    def __init__(self):
        self._route: list[Node] = []
        self._cost: float = 0.0

    def setNode(self, node: Node, cust: float):
        self._route.append(node)
        self._cost += cust

    def getCost(self):
        return self._cost

    def __str__(self) -> str:
        for position in range(len(self._route) - 1):
            print(
                self._route[position].id,
                end=" -> ",
            )

        print(self._route[-1])

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
