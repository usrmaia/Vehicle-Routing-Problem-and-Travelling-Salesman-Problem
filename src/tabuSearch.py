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
        initial_solution_heuristics: InitialSolutionHeuristics,
        neighborhood_heuristics: List[NeighborhoodHeuristic],
    ):
        # seed(42)
        self._tabu_list = TabuList(tabu_list_size)

        self._iteration = 0
        self._max_iteration = max_iterations

        self.initial_solution_heuristics = initial_solution_heuristics
        self.neighborhood_heuristics = neighborhood_heuristics

        self.intance_lower_bound = intance_lower_bound

        self.nodes = nodes
        self.graph = Graph()
        self.best_route = Route()

        self.tabuSearch()

    def initialSolution(self, num_solution) -> Route:
        candidates: List[Route] = [Route()] * num_solution

        for i in range(num_solution):
            match self.initial_solution_heuristics:
                case InitialSolutionHeuristics.RANDOMINSERTION:
                    candidates[i] = RandomInsertion(copy(self.nodes))
                case InitialSolutionHeuristics.NEARESTNEIGHBOR:
                    candidates[i] = NearestNeighbor(copy(self.nodes), self.graph)

        _, best = min(enumerate(candidates), key=lambda n: n[1].getCost())

        return best

    def tabuSearch(self):
        self.best_route = self.initialSolution(10)

        while not self.isStop():
            for i in range(1, len(self.best_route._route) - 1 - 1):
                j = randint(i + 1, len(self.best_route._route) - 1 - 1)

                if i == j:
                    continue

                heuristics = copy(self.neighborhood_heuristics)
                # heuristics = [Heuristic.TWOOPT]

                while heuristics:
                    heuristic = heuristics.pop(randrange(len(heuristics)))
                    self._iteration += 1

                    move = Move(heuristic, i, j)
                    if move in self._tabu_list:
                        continue

                    node_i, node_j = i, j
                    if heuristic != NeighborhoodHeuristic.OROPT and j < i:
                        node_i, node_j = j, i

                    # Pesquisa do custo
                    match heuristic:
                        case NeighborhoodHeuristic.SWAP:
                            cost = SwapCalculateCost(self.best_route, node_i, node_j, self.graph)
                        case NeighborhoodHeuristic.TWOOPT:
                            cost = TwoOPTCalculateCost(self.best_route, node_i, node_j, self.graph)
                        case NeighborhoodHeuristic.OROPT:
                            cost = OrOPTCalculateCost(self.best_route, node_i, node_j, self.graph)

                    # if cost > limit:
                    if cost > self.best_route.getCost():
                        self._tabu_list.append(move)
                        continue

                    # Atualização do custo
                    self.best_route._cost = cost

                    match heuristic:
                        case NeighborhoodHeuristic.SWAP:
                            route = SwapCalculateRoute(self.best_route, node_i, node_j)
                        case NeighborhoodHeuristic.TWOOPT:
                            route = TwoOPTCalculateRoute(
                                self.best_route, node_i, node_j
                            )
                        case NeighborhoodHeuristic.OROPT:
                            route = OrOPTCalculateRoute(self.best_route, node_i, node_j)

                    self.best_route._route = route
                    self._iteration = 0
                    heuristics = []

    def isStop(self) -> bool:
        # return True
        return self._iteration > self._max_iteration
        # return self.best_route.getCost() <= self._lower_bound * 1.05

        # if self.best_route.getCost() <= self._lower_bound * 1.05:
        #     return self._iteration > self._max_iterations

        # return False

    def getRoute(self) -> Route:
        self.best_route.calculateTotalCost(self.graph)

        return self.best_route


class Move:
    def __init__(
        self,
        heuristic: NeighborhoodHeuristic,
        i: int,
        j: int,
        segment=None,
    ) -> None:
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

        if move.heuristic != NeighborhoodHeuristic.OROPT:
            move = Move(move.heuristic, move.i, move.j)

        self._tabu_list[move] = True

    def __contains__(self, move: Move):
        if move.heuristic == NeighborhoodHeuristic.OROPT:
            return move in self._tabu_list

        return (
            Move(move.heuristic, move.i, move.j) in self._tabu_list
            or Move(move.heuristic, move.j, move.i) in self._tabu_list
        )
