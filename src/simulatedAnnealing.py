from copy import copy
from random import choice, randint
from typing import List
from graph import Graph
from heuristics import InitialSolutionHeuristics, NearestNeighbor, NeighborhoodHeuristic, RandomInsertion
from node import Node
from route import Route


class SimulatedAnnealing:
    def __init__(
        self,
        nodes: List[Node],
        intance_lower_bound: float,
        max_iterations: int,
        initial_solution_heuristics: InitialSolutionHeuristics,
        neighborhood_heuristics: List[NeighborhoodHeuristic],
        initial_temperature: float,
        alpha: float
    ):
        self._iteration = 0
        self._max_iteration = max_iterations

        self.initial_solution_heuristics = initial_solution_heuristics
        self.neighborhood_heuristics = neighborhood_heuristics

        self.intance_lower_bound = intance_lower_bound

        self.nodes = nodes
        self.graph = Graph()
        self.best_route = Route()

        self._initial_temperature = initial_temperature
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
        self.best_route = self.initialSolution(10)

        while not self.isStop():
            for i in range(1, len(self.best_route._route) - 1 - 1):
                j = randint(i + 1, len(self.best_route._route) - 1 - 1)

                if i == j:
                    continue

                heuristics = copy(self.neighborhood_heuristics)

                while len(heuristics) > 0:
                    neighborhood_heuristic = choice(heuristics)
                    heuristics.remove(neighborhood_heuristic)

                    new_route = neighborhood_heuristic(
                        copy(self.best_route), i, j
                    )

                    if self.acceptanceProbability(new_route.getCost(), self.best_route.getCost()) > random():
                        self.best_route = new_route
                        break

            self._iteration += 1
    
    def isStop(self) -> bool:
        return self._iteration >= self._max_iteration
        
