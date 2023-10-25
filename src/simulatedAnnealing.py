from copy import copy
from math import exp
from random import choice, randint, randrange
import random
from typing import List
from graph import Graph
from heuristics import (
    InitialSolutionHeuristics,
    NearestNeighbor,
    NeighborhoodHeuristic,
    OrOPTCalculateCost,
    OrOPTCalculateRoute,
    RandomInsertion,
    SwapCalculateCost,
    SwapCalculateRoute,
    TwoOPTCalculateCost,
    TwoOPTCalculateRoute,
)
from node import Node
from route import Route


class SimulatedAnnealing:
    def __init__(
        self,
        nodes: List[Node],
        intance_lower_bound: float,
        initial_solution_heuristics: InitialSolutionHeuristics,
        neighborhood_heuristics: List[NeighborhoodHeuristic],
        initial_temperature: float,
        alpha: float,
    ):
        self.initial_solution_heuristics = initial_solution_heuristics
        self.neighborhood_heuristics = neighborhood_heuristics

        self.intance_lower_bound = intance_lower_bound

        self.nodes = nodes
        self.graph = Graph()
        self.best_route = Route()

        self._temperature = initial_temperature
        self._alpha = alpha

        self.simulatedAnnealing()

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

    def simulatedAnnealing(self):
        self.best_route = self.initialSolution(5)

        while not self.isStop():
            for i in range(1, len(self.best_route._route) - 1 - 1 - 1):
                j = randint(i + 1, len(self.best_route._route) - 1 - 1)

                if i == j:
                    continue

                heuristics = copy(self.neighborhood_heuristics)

                while len(heuristics) > 0:
                    heuristic = heuristics.pop(randrange(len(heuristics)))

                    node_i, node_j = i, j
                    if heuristic != NeighborhoodHeuristic.OROPT and j < i:
                        node_i, node_j = j, i

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

                    if self.acceptanceProbability(cost, self.best_route.getCost()):
                        # Atualização do custo
                        self.best_route._cost = cost

                        match heuristic:
                            case NeighborhoodHeuristic.SWAP:
                                route = SwapCalculateRoute(
                                    self.best_route, node_i, node_j
                                )
                            case NeighborhoodHeuristic.TWOOPT:
                                route = TwoOPTCalculateRoute(
                                    self.best_route, node_i, node_j
                                )
                            case NeighborhoodHeuristic.OROPT:
                                route = OrOPTCalculateRoute(
                                    self.best_route, node_i, node_j
                                )

                        self.best_route._route = route
                        heuristic = []

    def acceptanceProbability(self, new_cost: float, old_cost: float) -> bool:
        if new_cost < old_cost:
            return True

        return exp((old_cost - new_cost) / self._temperature) > random.random()

    def isStop(self) -> bool:
        self._temperature *= self._alpha
        return self._temperature <= 0.0000000000000000000000000000000000000001

    def getRoute(self) -> Route:
        return self.best_route
