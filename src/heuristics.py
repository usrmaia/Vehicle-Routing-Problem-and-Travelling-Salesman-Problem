from enum import Enum
from typing import List
from random import randint
from node import Node
from route import Route


def RandomInsertion(nodes: List[Node]) -> Route:
    depot = nodes.pop(0)
    route = Route()
    route.setNode(depot)

    while len(nodes):
        node = nodes.pop(randint(0, len(nodes) - 1))
        route.setNode(node)

    route.setNode(depot)
    route.calculateTotalCost()

    return route


def NearestNeighbor(nodes: List[Node]) -> Route:
    depot = nodes.pop(0)
    route = Route()
    route.setNode(depot)
    # Adiciona um nó aleatório após o depot para iniciar o NN
    route.setNode(nodes.pop(randint(0, len(nodes) - 1)))

    while len(nodes):
        nearest_node_index, nearest_node = min(
            enumerate(nodes), key=lambda n: n[1].distanceTo(route._route[-1])
        )
        route.setNode(nearest_node)
        del nodes[nearest_node_index]

    route.setNode(depot)
    route.calculateTotalCost()

    return route


def SwapCalculateCost(route: Route, i: int, j: int) -> float:
    cost = route.getCost()

    cost -= route._route[i - 1].distanceTo(route._route[i])
    cost -= route._route[i].distanceTo(route._route[i + 1])

    if not i + 1 == j:
        cost -= route._route[j - 1].distanceTo(route._route[j])

    cost -= route._route[j].distanceTo(route._route[j + 1])

    #

    cost += route._route[i - 1].distanceTo(route._route[j])

    if not i + 1 == j:
        cost += route._route[j].distanceTo(route._route[i + 1])
        cost += route._route[j - 1].distanceTo(route._route[i])
    else:
        cost += route._route[j].distanceTo(route._route[i])

    cost += route._route[i].distanceTo(route._route[j + 1])

    return cost


def SwapCalculateRoute(route: Route, i: int, j: int) -> List[Node]:
    route._route[i], route._route[j] = route._route[j], route._route[i]

    return route._route


def TwoOPTCalculateCost(route: Route, i: int, j: int) -> float:
    cost = route.getCost()

    cost -= route._route[i - 1].distanceTo(route._route[i])
    cost -= route._route[j].distanceTo(route._route[j + 1])

    #

    cost += route._route[i - 1].distanceTo(route._route[j])
    cost += route._route[i].distanceTo(route._route[j + 1])

    return cost


def TwoOPTCalculateRoute(route: Route, i: int, j: int) -> List[Node]:
    route._route = (
        route._route[:i] + route._route[j : i - 1 : -1] + route._route[j + 1 :]
    )

    return route._route


def OrOPTCalculateCost(route: Route, i: int, j: int, segment: int = 0) -> float:
    cost = route.getCost()

    cost -= route._route[i - 1].distanceTo(route._route[i])
    cost -= route._route[i + segment].distanceTo(route._route[i + segment + 1])

    if i < j:
        cost -= route._route[j].distanceTo(route._route[j + 1])

        #

        cost += route._route[i - 1].distanceTo(route._route[i + segment + 1])
        cost += route._route[j].distanceTo(route._route[i])
        cost += route._route[i + segment].distanceTo(route._route[j + 1])
    elif i > j:
        cost -= route._route[j - 1].distanceTo(route._route[j])

        #

        cost += route._route[j - 1].distanceTo(route._route[i])
        cost += route._route[i + segment].distanceTo(route._route[j])
        cost += route._route[i - 1].distanceTo(route._route[i + segment + 1])

    return cost


def OrOPTCalculateRoute(route: Route, i: int, j: int, segment: int = 0) -> List[Node]:
    if i < j:
        route._route = (
            route._route[:i]
            + route._route[i + segment + 1 : j + 1]
            + route._route[i : i + segment + 1]
            + route._route[j + 1 :]
        )
    elif i > j:
        route._route = (
            route._route[:j]
            + route._route[i : i + segment + 1]
            + route._route[j:i]
            + route._route[i + segment + 1 :]
        )

    return route._route


class Heuristic(Enum):
    SWAP = 0
    TWOOPT = 1
    OROPT = 2
