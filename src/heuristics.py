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
    route.unsetCost(route._route[i - 1].distanceTo(route._route[i]))
    route.unsetCost(route._route[i].distanceTo(route._route[i + 1]))

    if not i + 1 == j:
        route.unsetCost(route._route[j - 1].distanceTo(route._route[j]))

    route.unsetCost(route._route[j].distanceTo(route._route[j + 1]))

    #

    route.setCost(route._route[i - 1].distanceTo(route._route[j]))

    if not i + 1 == j:
        route.setCost(route._route[j].distanceTo(route._route[i + 1]))
        route.setCost(route._route[j - 1].distanceTo(route._route[i]))
    else:
        route.setCost(route._route[j].distanceTo(route._route[i]))

    route.setCost(route._route[i].distanceTo(route._route[j + 1]))

    return route.getCost()


def SwapCalculateRoute(route: Route, i: int, j: int) -> Route:
    route._route[i], route._route[j] = route._route[j], route._route[i]

    return route


def TwoOPTCalculateCost(route: Route, i: int, j: int) -> float:
    route.unsetCost(route._route[i - 1].distanceTo(route._route[i]))
    route.unsetCost(route._route[j].distanceTo(route._route[j + 1]))

    #

    route.setCost(route._route[i - 1].distanceTo(route._route[j]))
    route.setCost(route._route[i].distanceTo(route._route[j + 1]))

    return route.getCost()


def TwoOPTCalculateRoute(route: Route, i: int, j: int) -> Route:
    route._route = (
        route._route[:i] + route._route[j : i - 1 : -1] + route._route[j + 1 :]
    )

    return route


def OrOPTCalculateCost(route: Route, i: int, j: int, segment: int = 0) -> float:
    route.unsetCost(route._route[i - 1].distanceTo(route._route[i]))
    route.unsetCost(route._route[i + segment].distanceTo(route._route[i + segment + 1]))

    if i < j:
        route.unsetCost(route._route[j].distanceTo(route._route[j + 1]))

        #

        route.setCost(route._route[i - 1].distanceTo(route._route[i + segment + 1]))
        route.setCost(route._route[j].distanceTo(route._route[i]))
        route.setCost(route._route[i + segment].distanceTo(route._route[j + 1]))
    elif i > j:
        route.unsetCost(route._route[j - 1].distanceTo(route._route[j]))

        #

        route.setCost(route._route[j - 1].distanceTo(route._route[i]))
        route.setCost(route._route[i + segment].distanceTo(route._route[j]))
        route.setCost(route._route[i - 1].distanceTo(route._route[i + segment + 1]))

    return route.getCost()


def OrOPTCalculateRoute(route: Route, i: int, j: int, segment: int = 0) -> Route:
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

    return route


def OrOPT(route: Route, i: int, j: int, segment: int = 0) -> Route:
    # i != depot ou i + segment != depot ou j != depot
    route.unsetCost(route._route[i - 1].distanceTo(route._route[i]))
    route.unsetCost(route._route[i + segment].distanceTo(route._route[i + segment + 1]))
    if i < j:
        route.unsetCost(route._route[j].distanceTo(route._route[j + 1]))
    elif i > j:
        route.unsetCost(route._route[j - 1].distanceTo(route._route[j]))

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

    if i < j:
        route.setCost(route._route[i - 1].distanceTo(route._route[i]))
        route.setCost(route._route[j].distanceTo(route._route[j + 1]))
        route.setCost(
            route._route[j - segment - 1].distanceTo(route._route[j - segment])
        )
    elif j < i:
        route.setCost(
            route._route[i + segment].distanceTo(route._route[i + segment + 1])
        )
        route.setCost(route._route[j - 1].distanceTo(route._route[j]))
        route.setCost(
            route._route[j + segment].distanceTo(route._route[j + segment + 1])
        )

    return route
