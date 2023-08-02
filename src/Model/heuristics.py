from typing import List
from .node import Node
from .route import Route

def RandomInsertion(self, nodes: List[Node]) -> Route:
    depot = nodes.pop[0]
    route: Route
    route.setNode(depot)

    while len(nodes):
        node = nodes.pop(randint(0, len(nodes) - 1))
        route.setNode(node)

    route.setNode(depot)
    route.calculateTotalCost()

    return route

def NearestNeighbor(self, nodes: List[Node]) -> Route:
    depot = nodes.pop[0]
    route: Route
    route.setNode(depot)
    # Adiciona um nó aleatório após o depot para iniciar o NN
    route.setNode(nodes.pop(randint(0, len(nodes) - 1)))

    while len(nodes):
        nearest_node_index, nearest_node = min(enumerate(nodes), key=lambda n: n[1].distanceTo(route[-1]))
        route.setNode(nearest_node)
        del nodes[nearest_node_index]

    route.setNode(depot)
    route.calculateTotalCost()

    return route

def Swap(route: Route, i: int, j: int) -> Route:
    route.unsetCost(route._route[i].distanceTo(route._route[i + 1]))
    route.unsetCost(route._route[i-1].distanceTo(route._route[i]))
    route.unsetCost(route._route[j].distanceTo(route._route[j+1]))
    route.unsetCost(route._route[j-1].distanceTo(route._route[j]))

    route._route[i], route._route[j] = route._route[j], route._route[i]

    route.setCost(route._route[i].distanceTo(route._route[i + 1]))
    route.setCost(route._route[i-1].distanceTo(route._route[i]))
    route.setCost(route._route[j].distanceTo(route._route[j+1]))
    route.setCost(route._route[j-1].distanceTo(route._route[j]))

    return route

def TwoOPT(route: Route, i: int, j: int) -> Route:
    route.unsetCost(route._route[i].distanceTo(route._route[i + 1]))
    route.unsetCost(route._route[j - 1].distanceTo(route._route[j]))

    route._route = (
        route._route[: i + 1]
        + route._route[j:i:-1]
        + route._route[j:]
    )

    route.setCost(route._route[i].distanceTo(route._route[i + 1]))
    route.setCost(route._route[j - 1].distanceTo(route._route[j]))

def OrOPT(route: Route, i: int, j: int, segment: int) -> Route:
    route.unsetCost(route._route[i - 1].distanceTo(route._route[i]))
    route.unsetCost(route._route[i + segment].distanceTo(route._route[i + segment + 1]))
    route.unsetCost(route._route[j].distanceTo(route._route[j + 1]))

    route._route = (
        route._route[:i]
        + route._route[i + segment : j]
        + route._route[i : i + segment]
        + route._route[j :]
    )

    route.setCost(route._route[i - 1].distanceTo(route._route[i]))
    route.setCost(route._route[i + segment].distanceTo(route._route[i + segment + 1]))
    route.setCost(route._route[j].distanceTo(route._route[j + 1]))

    