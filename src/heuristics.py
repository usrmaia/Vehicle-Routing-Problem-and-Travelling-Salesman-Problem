from enum import Enum
from typing import List
from random import randint
from graph import Graph
from node import Node
from route import Route


def RandomInsertion(nodes: List[Node], graph: Graph) -> Route:
    route = Route()

    depot = nodes.pop(0)
    route.addNode(depot)
    while len(nodes):
        node = nodes.pop(randint(0, len(nodes) - 1))
        route.addNode(node)
    route.addNode(depot)

    route.calculateTotalCost(graph)

    return route


def NearestNeighbor(nodes: List[Node], graph: Graph) -> Route:
    route = Route()

    depot = nodes.pop(0)
    route.addNode(depot)
    # Adiciona um nó aleatório após o depot para iniciar o NN
    route.addNode(nodes.pop(randint(0, len(nodes) - 1)))
    while len(nodes):
        # Encontra o nó mais próximo do último nó adicionado
        nearest_node_index, nearest_node = min(
            enumerate(nodes), key=lambda n: graph.distanceTo(route._route[-1], n[1])
        )
        route.addNode(nearest_node)
        nodes.pop(nearest_node_index)
    route.addNode(depot)

    route.calculateTotalCost(graph)

    return route


def SwapCalculateCost(route: Route, i: int, j: int, graph: Graph) -> float:
    cost = route.getCost()

    cost -= graph.distanceTo(route._route[i - 1], route._route[i])
    cost -= graph.distanceTo(route._route[i], route._route[i + 1])

    if not i + 1 == j:
        cost -= graph.distanceTo(route._route[j - 1], route._route[j])

    cost -= graph.distanceTo(route._route[j], route._route[j + 1])

    #

    cost += graph.distanceTo(route._route[i - 1], route._route[j])

    if not i + 1 == j:
        cost += graph.distanceTo(route._route[j], route._route[i + 1])
        cost += graph.distanceTo(route._route[j - 1], route._route[i])
    else:
        cost += graph.distanceTo(route._route[j], route._route[i])

    cost += graph.distanceTo(route._route[i], route._route[j + 1])

    return cost


def SwapCalculateRoute(route: Route, i: int, j: int) -> Route:
    route._route[i], route._route[j] = route._route[j], route._route[i]

    return route._route


def TwoOPTCalculateCost(route: Route, i: int, j: int, graph: Graph) -> float:
    cost = route.getCost()

    cost -= graph.distanceTo(route._route[i - 1], route._route[i])
    cost -= graph.distanceTo(route._route[j], route._route[j + 1])

    #

    cost += graph.distanceTo(route._route[i - 1], route._route[j])
    cost += graph.distanceTo(route._route[i], route._route[j + 1])

    return cost


def TwoOPTCalculateRoute(route: Route, i: int, j: int) -> List[Node]:
    route._route = (
        route._route[:i] + route._route[j : i - 1 : -1] + route._route[j + 1 :]
    )

    return route._route


def OrOPTCalculateCost(
    route: Route, i: int, j: int, graph: Graph, segment: int = 0
) -> float:
    cost = route.getCost()

    cost -= graph.distanceTo(route._route[i - 1], route._route[i])
    cost -= graph.distanceTo(route._route[i + segment], route._route[i + segment + 1])

    if i < j:
        cost -= graph.distanceTo(route._route[j], route._route[j + 1])

        #

        cost += graph.distanceTo(route._route[i - 1], route._route[i + segment + 1])
        cost += graph.distanceTo(route._route[j], route._route[i])
        cost += graph.distanceTo(route._route[i + segment], route._route[j + 1])
    elif i > j:
        cost -= graph.distanceTo(route._route[j - 1], route._route[j])

        #

        cost += graph.distanceTo(route._route[j - 1], route._route[i])
        cost += graph.distanceTo(route._route[i + segment], route._route[j])
        cost += graph.distanceTo(route._route[i - 1], route._route[i + segment + 1])

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


class NeighborhoodHeuristic(Enum):
    SWAP = 0
    TWOOPT = 1
    OROPT = 2


class InitialSolutionHeuristics(Enum):
    RANDOMINSERTION = 0
    NEARESTNEIGHBOR = 1
