from copy import copy
from random import seed
import sys
from typing import List
from time import time
from geneticAlgorithm import GeneticAlgorithm
from simulatedAnnealing import SimulatedAnnealing
from tabuSearch import TabuSearch
from heuristics import *
from route import Route
from node import Node
from inputDataFrame import DataFrame

medium_time = 0
min_time = sys.maxsize
max_time = 0
medium_cost = 0
min_cost = sys.maxsize
max_cost = 0

for i in range(1, 11):
    print(i)
    time0 = time()
    nodes: List[Node] = []
    nodes, lower_bound = DataFrame(
        "C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\u2319.tsp"
        # "C:\\Users\\konstroi.dev\\Codes\\Vehicle-Routing-Problem-and-Travelling-Salesman-Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\vm1084.tsp"
        # "/workspaces/Vehicle-Routing-Problem-and-Travelling-Salesman-Problem/Data Set/DIMACS-TSPLIB-Benchmark/my10.tsp"
        # "C:\\Users\\konstroi.dev\\Codes\\Vehicle-Routing-Problem-and-Travelling-Salesman-Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\my10.tsp"
    ).getDataFrame()

    route: Route = TabuSearch(
        nodes,
        lower_bound,
        3 * len(nodes) + 3,
        len(nodes) * 80,
        InitialSolutionHeuristics.NEARESTNEIGHBOR,
        [
            NeighborhoodHeuristic.SWAP,
            NeighborhoodHeuristic.TWOOPT,
            NeighborhoodHeuristic.OROPT,
        ],
    ).getRoute()
    """
    route: Route = SimulatedAnnealing(
        nodes,
        lower_bound,
        len(nodes) * 80,
        InitialSolutionHeuristics.NEARESTNEIGHBOR,
        [
            NeighborhoodHeuristic.SWAP,
            NeighborhoodHeuristic.TWOOPT,
            NeighborhoodHeuristic.OROPT,
        ],
        1000,
        0.99,
    ).getRoute()
    
    route: Route = GeneticAlgorithm(
        nodes=nodes,
        intance_lower_bound=lower_bound,
        initial_solution_heuristic=InitialSolutionHeuristics.NEARESTNEIGHBOR,
        neighborhood_heuristics=[
            NeighborhoodHeuristic.SWAP,
            NeighborhoodHeuristic.TWOOPT,
            NeighborhoodHeuristic.OROPT,
        ],
        max_generations=100,
        population_size=20,
        crossover_probability=50,
        mutation_probability=5,
        elitis=20,
        max_time=100,
    ).getRoute()
    """
    time1 = time()
    medium_time += time1 - time0
    if time1 - time0 < min_time:
        min_time = time1 - time0
    if time1 - time0 > max_time:
        max_time = time1 - time0

    medium_cost += route.getCost()
    if route.getCost() < min_cost:
        min_cost = route.getCost()
    if route.getCost() > max_cost:
        max_cost = route.getCost()

    graph: Graph = Graph()
    if round(route.getCost(), 2) != round(route.calculateTotalCost(graph), 2):
        raise Exception("Cost is not equal to calculateTotalCost")
    if len(route._route) != len(nodes) + 1:
        raise Exception("Route is not equal to nodes")

print("Tabu Search - 3 * len(nodes) + 3, 40 - vm1084")
print("vm1084")
print(f"Tempo médio de execução: {medium_time / 10}...")
print(f"Tempo mínimo de execução: {min_time}...")
print(f"Tempo máximo de execução: {max_time}...")
print(f"Custo médio do custo: {medium_cost / 10}...")
print(f"Custo mínimo do custo: {min_cost}...")
print(f"Custo máximo do custo: {max_cost}...")
