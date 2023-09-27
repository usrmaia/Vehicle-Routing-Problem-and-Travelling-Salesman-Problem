from copy import copy
from random import choice, choices, randint
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
        self.elitis: int = elitis

        self.max_time: int = max_time

        self.best_generation: List[Route] = List[Route]
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
        self.best_generation = self.best_generation[: self.elitis]
        # """

        # Roulette
        """
        total_fitness = sum(route.getCost() for route in self.best_generation)
        probabilities = [
            route.getCost() / total_fitness for route in self.best_generation
        ]
        self.best_generation = choices(
            self.best_generation, weights=probabilities, k=self.elitis
        )
        """

        self.best_route = self.best_generation[0]

    def fitness(self):
        self.best_generation.sort(key=lambda route: route.getCost())

    def generateInitialPopulation(self) -> None:
        routes: List[Route] = []

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
        childs: List[Route] = []

        for route in self.best_generation:
            # Bests have more chance to crossover
            weight = 1 - (route.getCost() - min_fitness) / (max_fitness - min_fitness)

            if self.crossover_probability * weight < randint(0, 100):
                continue

            parent_1 = route
            rand_parent = choices(self.best_generation, weights=fitness_values.reverse())[0]
            parent_2 = rand_parent

            def breed(parent_1: Route, parent_2: Route) -> Route:
                gene_A = randint(1, len(parent_1._route) - 1 - 1 - 1)
                gene_B = randint(gene_A, len(parent_1._route) - 1 - 1)
                
                start_gene = min(gene_A, gene_B)
                end_gene = max(gene_A, gene_B)

                child_2: List[Node] = parent_1._route[start_gene:end_gene + 1]
                
                child_1: List[Node] = []
                for node in parent_2._route[:start_gene]:
                    if node in child_2:
                        start_gene += 1
                    child_1.append(node)
                
                child_3: List[Node] = []
                for node in parent_2._route[start_gene:]:
                    if node in child_2:
                        start_gene += 1
                    child_3.append(node)
                
                child: Route = Route()
                child._route = child_1 + child_2 + child_3
                child._cost = child.calculateTotalCost(self.graph)

                return child

            child = breed(parent_1, parent_2)
            childs.append(child)
        
        self.best_generation.extend(childs)

    def mutation(self) -> None:
        new_routes: List[Route] = []

        for route in self.best_generation:
            if self.mutation_probability < randint(0, 100): 
                continue

            route: Route = Route()
            node_i = randint(1, len(self.best_route._route) - 1 - 1)
            node_j = randint(node_i, len(self.best_route._route) - 1 - 1)

            if NeighborhoodHeuristic.SWAP in self.neighborhood_heuristics:
                route._cost = SwapCalculateCost(
                    copy(self.best_route), node_i, node_j, self.graph
                )
                route._route = SwapCalculateRoute(copy(self.best_route), node_i, node_j)
                new_routes.append(route)
            if NeighborhoodHeuristic.TWOOPT in self.neighborhood_heuristics:
                route._cost = TwoOPTCalculateCost(
                    copy(self.best_route), node_i, node_j, self.graph
                )
                route._route = TwoOPTCalculateRoute(
                    copy(self.best_route), node_i, node_j
                )
                new_routes.append(route)
            if NeighborhoodHeuristic.OROPT in self.neighborhood_heuristics:
                route._cost = OrOPTCalculateCost(
                    copy(self.best_route), node_i, node_j, self.graph
                )
                route._route = OrOPTCalculateRoute(
                    copy(self.best_route), node_i, node_j
                )
                new_routes.append(route)

        self.best_generation.extend(new_routes)

    def getRoute(self) -> Route:
        return self.best_route
