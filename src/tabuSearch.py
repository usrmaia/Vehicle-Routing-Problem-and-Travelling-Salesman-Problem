from collections import deque
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
                    candidates[i] = RandomInsertion(copy(self.nodes), self.graph)
                case InitialSolutionHeuristics.NEARESTNEIGHBOR:
                    candidates[i] = NearestNeighbor(copy(self.nodes), self.graph)

        _, best = min(enumerate(candidates), key=lambda n: n[1].getCost())

        return best

    def tabuSearch(self):
        self.best_route = self.initialSolution(10)
        print("Initial solution")

        while not self.isStop():
            for i in range(1, len(self.best_route._route) - 1 - 1 - 1):
                self._iteration += 1

                j = randrange(i + 1, len(self.best_route._route) - 1 - 1)

                if i == j:
                    continue

                heuristics = copy(self.neighborhood_heuristics)

                while heuristics:
                    heuristic = heuristics.pop(randrange(len(heuristics)))

                    move = Move(self.best_route, heuristic, i, j)
                    if move in self._tabu_list:
                        continue

                    node_i, node_j = i, j

                    # Pesquisa do custo
                    match heuristic:
                        case NeighborhoodHeuristic.SWAP:
                            cost = SwapCalculateCost(
                                self.best_route, node_i, node_j, self.graph
                            )
                        case NeighborhoodHeuristic.TWOOPT:
                            cost = TwoOPTCalculateCost(
                                self.best_route, node_i, node_j, self.graph
                            )
                        case NeighborhoodHeuristic.OROPT:
                            cost = OrOPTCalculateCost(
                                self.best_route, node_i, node_j, self.graph
                            )

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
                    heuristics = []
                    self._iteration = 0

    def isStop(self) -> bool:
        # return True
        return self._iteration > self._max_iteration
        # return self.best_route.getCost() <= self._lower_bound * 1.05

        # if self.best_route.getCost() <= self._lower_bound * 1.05:
        #     return self._iteration > self._max_iterations

        # return False

    def getRoute(self) -> Route:
        return self.best_route


class Move:
    def __init__(
        self, route: Route, heuristic: NeighborhoodHeuristic, i: int, j: int
    ) -> None:
        self.cost = route._cost
        self.heuristic = heuristic
        self.i = i
        self.j = j

    def __eq__(self, __value: "Move") -> bool:
        return (
            self.cost == __value.cost
            and self.heuristic == __value.heuristic
            and self.i == __value.i
            and self.j == __value.j
        )

    def __hash__(self) -> int:
        return hash((self.cost, self.heuristic, self.i, self.j))


class TabuList:
    def __init__(self, max_len):
        self._tabu_set = set()
        self.max_len = max_len

    def append(self, move):
        if len(self._tabu_set) > self.max_len:
            self._tabu_set.clear()

        move_hash = hash(move)
        self._tabu_set.add(move_hash)

    def __contains__(self, move):
        move_hash = hash(move)
        return move_hash in self._tabu_set
