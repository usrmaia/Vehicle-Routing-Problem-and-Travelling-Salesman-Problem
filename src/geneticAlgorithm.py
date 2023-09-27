from copy import copy
from random import choices, randint
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


class GeneticAlgorithm:
    def __init__(
        self,
        nodes: List[Node],
        intance_lower_bound: float,
        initial_solution_heuristic: InitialSolutionHeuristics,
        neighborhood_heuristics: List[NeighborhoodHeuristic],
        max_generations: int,
        population_size: int,
        crossover_probability: float,
        mutation_probability: float,
        elitis: float,
        max_time: int,
    ):
        self.nodes: List[Node] = nodes
        self.intance_lower_bound: float = intance_lower_bound
        self.initial_solution_heuristic = initial_solution_heuristic
        self.neighborhood_heuristics = neighborhood_heuristics

        self.max_generations: int = max_generations
        self.population_size: int = population_size

        self.crossover_probability: float = crossover_probability
        self.mutation_probability: float = mutation_probability
        self.elitis: float = elitis

        self.max_time: int = max_time

        self.best_generation: List[Route] = List[Route]()
        self.best_route: Route = Route()
        self.graph: Graph = Graph()

        self.geneticAlgorithm()

    def geneticAlgorithm(self) -> None:
        self.generateInitialPopulation()

        self.fitness()
        self.selection()

        while not self.isStop():  # Converege
            self.crossover()
            self.mutation()

            self.fitness()
            self.selection()

    def selection(self):
        # Elitism
        # """
        self.best_generation = self.best_generation[
            : int(self.elitis * len(self.best_generation))
        ]
        # """

        # Roulette
        """
        total_fitness = sum(route.getCost() for route in self.best_generation)
        probabilities = [
            route.getCost() / total_fitness for route in self.best_generation
        ]
        self.best_generation = choices(
            self.best_generation, weights=probabilities, k=self.population_size
        )
        """

        self.best_route = self.best_generation[0]

    def fitness(self):
        self.best_generation.sort(key=lambda route: route.getCost())

    def generateInitialPopulation(self) -> None:
        routes: List[Route] = List[Route]()

        for _ in range(self.population_size):
            match self.initial_solution_heuristic:
                case InitialSolutionHeuristics.RANDOMINSERTION:
                    routes.append(RandomInsertion(copy(self.nodes)))
                case InitialSolutionHeuristics.NEARESTNEIGHBOR:
                    routes.append(NearestNeighbor(copy(self.nodes), self.graph))

        self.best_generation = routes

    def isStop(self) -> bool:
        if (
            self.best_route.getCost() <= self.intance_lower_bound
            # or self.max_time <= 0
            or self.max_generations <= 0
        ):
            return True

        self.max_generations -= 1

        return False

    def crossover(self) -> None:
        fitness_values = [route.getCost() for route in self.best_generation]
        min_fitness = min(fitness_values)
        max_fitness = max(fitness_values)

        for i in range(self.population_size - len(self.best_generation)):
            if self.crossover_probability * (
                1 + (fitness_values[i] - min_fitness) / (max_fitness - min_fitness)
            ) < randint(0, 100):
                continue

            rand_parent = randint(1, len(self.best_generation) - 1 - 1)
            parent_1 = self.best_generation[i]
            parent_2 = self.best_generation[rand_parent]

            rand_cut = randint(1, len(parent_1._route) - 1 - 1)
            child_1 = Route()
            child_1._route = parent_1._route[:rand_cut] + parent_2._route[rand_cut:]
            child_2 = Route()
            child_2._route = parent_2._route[:rand_cut] + parent_1._route[rand_cut:]

            def childCorrection(child_1: Route, child_2: Route) -> (Route, Route):
                for node in child_1._route[1:-1]:
                    if child_1._route.count(node) > 1:
                        child_1._route.remove(node)

                for node in self.nodes[1:]:
                    if node not in child_1._route:
                        child_1._route.append()

                for node in child_2._route[1:-1]:
                    if child_2._route.count(node) > 1:
                        child_2._route.remove(node)

                return child_1, child_2

    def mutation(self) -> None:
        new_routes: List[Route] = List[Route]()

        for route in self.best_generation:
            if self.mutation_probability > randint(0, 100):
                continue

            route: Route = Route()
            node_i = randint(1, len(self.best_route._route) - 1 - 1)
            node_j = randint(node_i, len(self.best_route._route) - 1 - 1)

            if NeighborhoodHeuristic.SWAP in self.neighborhood_heuristics:
                route._cost = SwapCalculateCost(
                    self.best_route, node_i, node_j, self.graph
                )
                route._route = SwapCalculateRoute(copy(self.best_route), node_i, node_j)
                new_routes.append(route)
            if NeighborhoodHeuristic.TWOOPT in self.neighborhood_heuristics:
                route._cost = TwoOPTCalculateCost(
                    self.best_route, node_i, node_j, self.graph
                )
                route._route = TwoOPTCalculateRoute(
                    copy(self.best_route), node_i, node_j
                )
                new_routes.append(route)
            if NeighborhoodHeuristic.OROPT in self.neighborhood_heuristics:
                route._cost = OrOPTCalculateCost(
                    self.best_route, node_i, node_j, self.graph
                )
                route._route = OrOPTCalculateRoute(
                    copy(self.best_route), node_i, node_j
                )
                new_routes.append(route)

        self.best_generation.extend(new_routes)

    def getRoute(self) -> Route:
        return self.best_route
