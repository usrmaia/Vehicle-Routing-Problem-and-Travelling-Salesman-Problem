from sys import maxsize
from random import randint, seed, choice, randrange
from copy import copy
from typing import List
from enum import Enum
from node import Node
from route import Route
from heuristics import *


class TabuSearch:
    def __init__(
        self,
        nodes: List[Node],
        intance_lower_bound: float,
        tabu_list_size: int,
        max_iterations: int,
    ):
        # seed(42)
        self._tabu_list = TabuList(tabu_list_size)

        self._iteration = 0
        self._max_iteration = max_iterations

        self.intance_lower_bound = intance_lower_bound

        self.nodes = nodes
        self.best_route = Route()

        self.tabuSearch()

    def initialSolution(self, num_solution) -> Route:
        candidates: List[Route] = [Route()] * num_solution

        for i in range(num_solution):
            candidates[i] = NearestNeighbor(copy(self.nodes))
            # candidates[i] = RandomInsertion(copy(self.nodes))

        _, best = min(enumerate(candidates), key=lambda n: n[1].getCost())

        return best

    def tabuSearch(self):
        self.best_route = self.initialSolution(10)

        num_swap, num_twoopt, num_oropt = 0, 0, 0

        while not self.isStop():
            for i in range(1, len(self.best_route._route) - 1):
                j = randint(1, len(self.best_route._route) - 1 - 1)

                if i == j:
                    continue

                heuristics = [Heuristic.SWAP, Heuristic.TWOOPT, Heuristic.OROPT]
                # heuristics = [Heuristic.TWOOPT]

                while heuristics:
                    heuristic = heuristics.pop(randrange(len(heuristics)))
                    self._iteration += 1

                    move = Move(self.best_route, heuristic, i, j)
                    if move in self._tabu_list:
                        continue

                    node_i, node_j = i, j
                    if heuristic != Heuristic.OROPT and j < i:
                        node_i, node_j = j, i

                    # Pesquisa do custo
                    match heuristic:
                        case Heuristic.SWAP:
                            cost = SwapCalculateCost(self.best_route, node_i, node_j)
                        case Heuristic.TWOOPT:
                            cost = TwoOPTCalculateCost(self.best_route, node_i, node_j)
                        case Heuristic.OROPT:
                            cost = OrOPTCalculateCost(self.best_route, node_i, node_j)

                    # if cost > limit:
                    if cost > self.best_route.getCost():
                        self._tabu_list.append(move)
                        continue

                    # Atualização do custo
                    self.best_route._cost = cost

                    match heuristic:
                        case Heuristic.SWAP:
                            route = SwapCalculateRoute(self.best_route, node_i, node_j)
                            num_swap += 1
                        case Heuristic.TWOOPT:
                            route = TwoOPTCalculateRoute(
                                self.best_route, node_i, node_j
                            )
                            num_twoopt += 1
                        case Heuristic.OROPT:
                            route = OrOPTCalculateRoute(self.best_route, node_i, node_j)
                            num_oropt += 1

                    self.best_route._route = route
                    self._iteration = 0

        print(num_swap, num_twoopt, num_oropt)

    def isStop(self) -> bool:
        # return True
        return self._iteration > self._max_iteration
        # return self.best_route.getCost() <= self._lower_bound * 1.05

        # if self.best_route.getCost() <= self._lower_bound * 1.05:
        #     return self._iteration > self._max_iterations

        # return False

    def getRoute(self) -> Route:
        self.best_route.calculateTotalCost()

        return self.best_route


class Move:
    def __init__(
        self, route: Route, heuristic: Heuristic, i: int, j: int, segment=None
    ) -> None:
        self.route = route
        self.heuristic = heuristic
        self.i = i
        self.j = j
        self.segment = segment


class TabuList:
    def __init__(self, len) -> None:
        self._tabu_list = {}
        self._len = len

    def append(self, move: Move):
        # Manutenção do tamanho da lista
        if len(self._tabu_list) > self._len:
            self._tabu_list.clear()  # Abordagem que limpa a lista
            # self._tabu_list.pop(self._tabu_list.values()[0]) # Abordagem que remove o primeiro elemento

        if move.heuristic != Heuristic.OROPT:
            move = Move(move.route, move.heuristic, move.i, move.j)

        self._tabu_list[move] = True

    def __contains__(self, move: Move):
        if move.heuristic == Heuristic.OROPT:
            return move in self._tabu_list

        return Move(move.route, move.heuristic, move.i, move.j) in self._tabu_list
