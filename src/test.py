import pytest
from random import seed
from typing import List
from heuristics import *
from node import Node
from route import Route


lower_bound = 40.59
nodes: List[Node] = [
    Node(1, 5, 5),
    Node(2, 0, 4),
    Node(3, 2, 0),
    Node(4, 5, 1),
    Node(5, 10, 1),
    Node(6, 2, 8),
    Node(7, 6, 10),
    Node(8, 7, 7),
    Node(9, 10, 6),
    Node(10, 9, 9),
]

random_nodes: List[Node] = [
    Node(1, 5, 5),
    Node(3, 2, 0),
    Node(2, 0, 4),
    Node(9, 10, 6),
    Node(6, 2, 8),
    Node(5, 10, 1),
    Node(7, 6, 10),
    Node(4, 5, 1),
    Node(8, 7, 7),
    Node(10, 9, 9),
    Node(1, 5, 5),
]


def testRandomInsertion():
    seed(42)

    route: Route = RandomInsertion(nodes.copy())

    assert route._route[0] == nodes[0]
    assert route._route[-1] == nodes[0]
    assert route.getCost() >= lower_bound
    assert route._route[0] not in route._route[1:-1]
    assert len(route._route) == len(nodes) + 1

    for i, n in enumerate(route._route):
        assert n in nodes
        assert route._route[i] == random_nodes[i]


nearest_nodes: List[Node] = [
    Node(1, 5, 5),
    Node(3, 2, 0),
    Node(4, 5, 1),
    Node(5, 10, 1),
    Node(9, 10, 6),
    Node(8, 7, 7),
    Node(10, 9, 9),
    Node(7, 6, 10),
    Node(6, 2, 8),
    Node(2, 0, 4),
    Node(1, 5, 5),
]


def testNearestNeighbor():
    seed(42)

    route: Route = NearestNeighbor(nodes.copy())

    assert route._route[0] == nodes[0]
    assert route._route[-1] == nodes[0]
    assert route.getCost() >= lower_bound
    assert len(route._route) == len(nodes) + 1

    for i, n in enumerate(route._route):
        assert n in nodes
        assert route._route[i] == nearest_nodes[i]


def testSwapCalculateCost():
    # Caso i e j, primeiro cliente e cliente consecutivo

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 1, 2
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)

    # Caso i e j, primeiro cliente e cliente qualquer

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(7, 6, 10),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 1, 6
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)

    # Caso i e j, primeiro cliente e último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(10, 9, 9),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 1, 9
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)

    # Caso i e j quaisquer, não consecutivos, nem primeiro e nem último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 2, 7
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)

    # Caso i e j quaisquer, consecutivos, nem primeiro e nem último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 4, 5
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)

    # Caso i e j, não consecutivos, cliente qualquer e último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(10, 9, 9),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(5, 10, 1),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 4, 9
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)

    # Caso i e j, consecutivos, penúltimo cliente e último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 8, 9
    route_swap0 = SwapCalculateCost(route_swap0, i, j)
    assert round(route_swap0, 4) == round(route_swap1.getCost(), 4)


def testSwapCalculateRoute():
    # Caso i e j, primeiro cliente e cliente consecutivo

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 1, 2
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()

    # Caso i e j, primeiro cliente e cliente qualquer

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(7, 6, 10),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 1, 6
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()

    # Caso i e j, primeiro cliente e último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(10, 9, 9),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 1, 9
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()

    # Caso i e j quaisquer, não consecutivos, nem primeiro e nem último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 2, 7
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()

    # Caso i e j quaisquer, consecutivos, nem primeiro e nem último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 4, 5
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()

    # Caso i e j, não consecutivos, cliente qualquer e último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(10, 9, 9),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(5, 10, 1),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 4, 9
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()

    # Caso i e j, consecutivos, penúltimo cliente e último cliente

    route_swap0 = Route()
    route_swap0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    i, j = 8, 9
    route_swap0 = SwapCalculateRoute(route_swap0, i, j)
    assert route_swap0.getRoute() == route_swap1.getRoute()


def testTwoOPTCalculateCost():
    # Caso i e j, primeiro cliente e cliente consecutivo

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 1, 2
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)

    # Caso i e j, primeiro cliente e cliente não consecutivo

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 1, 5
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)

    # Caso i e j, primeiro cliente e último cliente

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(8, 7, 7),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 1, 9
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)

    # Caso i e j, não consecutivo, clientes quaisquer

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 2, 7
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)

    # Caso i e j, clientes quaisquer consecutivos

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 4, 5
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)

    # Caso i e j, cliente qualquer e último cliente

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(8, 7, 7),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 5, 9
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)

    # Caso i e j, penúltimo cliente e último cliente

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 8, 9
    route_twoopt0 = TwoOPTCalculateCost(route_twoopt0, i, j)
    assert round(route_twoopt0, 4) == round(route_twoopt1.getCost(), 4)


def testTwoOPTCalculateRoute():
    # Caso i e j, primeiro cliente e cliente consecutivo

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 1, 2
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()

    # Caso i e j, primeiro cliente e cliente não consecutivo

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 1, 5
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()

    # Caso i e j, primeiro cliente e último cliente

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(8, 7, 7),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 1, 9
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()

    # Caso i e j, não consecutivo, clientes quaisquer

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 2, 7
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()

    # Caso i e j, clientes quaisquer consecutivos

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 4, 5
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()

    # Caso i e j, cliente qualquer e último cliente

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(8, 7, 7),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 5, 9
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()

    # Caso i e j, penúltimo cliente e último cliente

    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    i, j = 8, 9
    route_twoopt0 = TwoOPTCalculateRoute(route_twoopt0, i, j)
    assert route_twoopt0.getRoute() == route_twoopt1.getRoute()


def testOrOPTCalculateCost():
    # Caso i < j, primeiro cliente e cliente consecutivo sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 2, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e cliente consecutivo com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 3, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e cliente consecutivo com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 4, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 6, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 7, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e cliente qualquer com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 6, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 9, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e último cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 9, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e último cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 9, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, não consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(4, 5, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 6, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, não consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 2, 7, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, não consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 7, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 6, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(8, 7, 7),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 7, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(6, 2, 8),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 2, 5, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, penúltimo cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 9, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, triúltimo cliente e último cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 9, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, quatroúltimo cliente e último cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 9, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, último cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 9, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, último cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 4, 9, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i < j, primeiro cliente e cliente qualquer com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 9, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    #

    # Caso i > j, primeiro cliente e cliente consecutivo sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 2, 1, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e cliente consecutivo com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 1, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e cliente consecutivo com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 4, 1, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 1, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 1, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e cliente qualquer com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 1, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 9, 1, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e penúltimo cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 1, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, primeiro cliente e triúltimo cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 1, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, não consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 3, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, não consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 2, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, não consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 3, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 5, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 5, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 2, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, penúltimo cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 9, 8, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, triúltimo cliente e penúltimo cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(8, 7, 7),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 7, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, quatroúltimo cliente e triúltimo cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 6, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, último cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(10, 9, 9),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 9, 5, 0
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, penúltimo cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 4, 1
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)

    # Caso i > j, triúltimo cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 3, 2
    route_oropt0 = OrOPTCalculateCost(route_oropt0, i, j, s)
    assert round(route_oropt0, 4) == round(route_oropt1.getCost(), 4)


def testOrOPTCalculateRoute():
    # Caso i < j, primeiro cliente e cliente consecutivo sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 2, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e cliente consecutivo com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 3, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e cliente consecutivo com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 4, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 6, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 7, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e cliente qualquer com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 6, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 9, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e último cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 9, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e último cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 1, 9, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, não consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(4, 5, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 6, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, não consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 2, 7, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, não consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 7, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 6, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(8, 7, 7),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 7, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(6, 2, 8),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 2, 5, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, penúltimo cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 9, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, triúltimo cliente e último cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 9, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, quatroúltimo cliente e último cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 9, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, último cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 9, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, último cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 4, 9, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i < j, primeiro cliente e cliente qualquer com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 9, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    #

    # Caso i > j, primeiro cliente e cliente consecutivo sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 2, 1, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e cliente consecutivo com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 3, 1, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e cliente consecutivo com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 4, 1, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 1, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 1, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e cliente qualquer com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 1, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 9, 1, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e penúltimo cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 1, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, primeiro cliente e triúltimo cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 1, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, não consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 3, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, não consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 2, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, não consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 3, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, consecutivo, clientes quaisquer, sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(7, 6, 10),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 6, 5, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, consecutivo, clientes quaisquer, com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 5, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, consecutivo, clientes quaisquer, com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 5, 2, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, penúltimo cliente e último cliente sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 9, 8, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, triúltimo cliente e penúltimo cliente com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(8, 7, 7),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 7, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, quatroúltimo cliente e triúltimo cliente com segmento 2

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 6, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, último cliente e cliente qualquer sem segmento

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(10, 9, 9),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 9, 5, 0
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, penúltimo cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 8, 4, 1
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()

    # Caso i > j, triúltimo cliente e cliente qualquer com segmento 1

    route_oropt0 = Route()
    route_oropt0._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(1, 5, 5),
    ]
    route_oropt0.calculateTotalCost()

    route_oropt1 = Route()
    route_oropt1._route = [
        Node(1, 5, 5),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(8, 7, 7),
        Node(9, 10, 6),
        Node(10, 9, 9),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(7, 6, 10),
        Node(1, 5, 5),
    ]
    route_oropt1.calculateTotalCost()

    i, j, s = 7, 3, 2
    route_oropt0 = OrOPTCalculateRoute(route_oropt0, i, j, s)
    assert route_oropt0.getRoute() == route_oropt1.getRoute()


testRandomInsertion()
testNearestNeighbor()
testSwapCalculateCost()
testSwapCalculateRoute()
testTwoOPTCalculateCost()
testTwoOPTCalculateRoute()
testOrOPTCalculateCost()
testOrOPTCalculateRoute()
