import pytest
from random import seed
from typing import List
from Model.heuristics import *
from Model.node import Node
from Model.route import Route


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


def testSwap():
    route_swap0 = Route()
    route_swap0._route = [
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
    route_swap0.calculateTotalCost()

    route_swap1 = Route()
    route_swap1._route = [
        Node(1, 5, 5),
        Node(3, 2, 0),
        Node(4, 5, 1),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_swap1.calculateTotalCost()

    route_swap2 = Route()
    route_swap2._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_swap2.calculateTotalCost()

    route_swap3 = Route()
    route_swap3._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(4, 5, 1),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(2, 0, 4),
        Node(1, 5, 5),
    ]
    route_swap3.calculateTotalCost()

    route_swap4 = Route()
    route_swap4._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(4, 5, 1),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_swap4.calculateTotalCost()

    route_swap5 = Route()
    route_swap5._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(6, 2, 8),
        Node(4, 5, 1),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(2, 0, 4),
        Node(5, 10, 1),
        Node(1, 5, 5),
    ]
    route_swap5.calculateTotalCost()

    i, j = 4, 8
    route_swap0 = Swap(route_swap0, i, j)
    assert route_swap0 == route_swap1

    i, j = 1, 2
    route_swap1 = Swap(route_swap1, i, j)
    assert route_swap1 == route_swap2

    i, j = 1, 5
    route_swap2 = Swap(route_swap2, i, j)
    assert route_swap2 == route_swap3

    i, j = 8, 9
    route_swap3 = Swap(route_swap3, i, j)
    assert route_swap3 == route_swap4

    i, j = 3, 9
    route_swap4 = Swap(route_swap4, i, j)
    assert route_swap4 == route_swap5


def testTwoOPT():
    # A,H,J,G,D(i),F,E,B,C(j),I
    # A,H,J,G,C(i),B,E,F,D(j),I
    route_twoopt0 = Route()
    route_twoopt0._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(5, 10, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_twoopt0.calculateTotalCost()

    route_twoopt1 = Route()
    route_twoopt1._route = [
        Node(1, 5, 5),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(5, 10, 1),
        Node(6, 2, 8),
        Node(4, 5, 1),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_twoopt1.calculateTotalCost()

    route_twoopt2 = Route()
    route_twoopt2._route = [
        Node(1, 5, 5),
        Node(5, 10, 1),
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(7, 6, 10),
        Node(10, 9, 9),
        Node(8, 7, 7),
        Node(6, 2, 8),
        Node(4, 5, 1),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_twoopt2.calculateTotalCost()

    route_twoopt3 = Route()
    route_twoopt3._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(5, 10, 1),
        Node(9, 10, 6),
        Node(1, 5, 5),
    ]
    route_twoopt3.calculateTotalCost()

    route_twoopt4 = Route()
    route_twoopt4._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(5, 10, 1),  #
        Node(2, 0, 4),
        Node(3, 2, 0),
        Node(9, 10, 6),  #
        Node(1, 5, 5),
    ]
    route_twoopt4.calculateTotalCost()

    route_twoopt5 = Route()
    route_twoopt5._route = [
        Node(1, 5, 5),
        Node(4, 5, 1),
        Node(6, 2, 8),
        Node(8, 7, 7),
        Node(10, 9, 9),
        Node(7, 6, 10),
        Node(9, 10, 6),
        Node(3, 2, 0),
        Node(2, 0, 4),
        Node(5, 10, 1),
        Node(1, 5, 5),
    ]
    route_twoopt5.calculateTotalCost()

    i, j = 4, 8
    route_twoopt0 = TwoOPT(route_twoopt0, i, j)
    assert route_twoopt0 == route_twoopt1

    i, j = 1, 6
    route_twoopt1 = TwoOPT(route_twoopt1, i, j)
    assert route_twoopt1 == route_twoopt2

    i, j = 1, 8
    route_twoopt2 = TwoOPT(route_twoopt2, i, j)
    assert route_twoopt2 == route_twoopt3

    i, j = 6, 9
    route_twoopt4 = TwoOPT(route_twoopt4, i, j)
    assert route_twoopt4 == route_twoopt5

    pass


testRandomInsertion()
testNearestNeighbor()
testSwap()
testTwoOPT()
