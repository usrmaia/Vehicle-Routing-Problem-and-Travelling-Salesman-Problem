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
import statistics

instance = "ceara184"
"""
    "u1060",
    "vm1084",
    "fl1400",
    "u1432",
    "fl1577",
    "fl1577",
    "vm1748",
    "u2152",
    "u2319",
    "fl3795",
    "pla7397",
    "brd14051",
    "pla33810",
    "pla85900",
    "valedojaguaribe15",
    "valedojaguaribe21",
    "ceara184",
"""
metaheuristic = "SimulatedAnnealing"
"""
    "TabuSearch", 
    "SimulatedAnnealing", 
    "GeneticAlgorithm"
"""
# path = f"C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\{instance}.tsp"
# path = f"C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\Vale do Jaguaribe\\{instance}.tsp"
path = f"C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\Ceara\\{instance}.tsp"
times: List[float] = []
costs: List[float] = []

for i in range(1, 11):
    print(i)
    time0 = time()
    nodes: List[Node] = []

    nodes, lower_bound = DataFrame(
        path
        # "C:\\Users\\konstroi.dev\\Codes\\Vehicle-Routing-Problem-and-Travelling-Salesman-Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\vm1084.tsp"
        # "/workspaces/Vehicle-Routing-Problem-and-Travelling-Salesman-Problem/Data Set/DIMACS-TSPLIB-Benchmark/my10.tsp"
        # "C:\\Users\\konstroi.dev\\Codes\\Vehicle-Routing-Problem-and-Travelling-Salesman-Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\my10.tsp"
    ).getDataFrame()

    match metaheuristic:
        case "TabuSearch":
            route: Route = TabuSearch(
                nodes,
                lower_bound,
                3 * len(nodes) + 3,
                80000,
                InitialSolutionHeuristics.NEARESTNEIGHBOR,
                [
                    NeighborhoodHeuristic.SWAP,
                    NeighborhoodHeuristic.TWOOPT,
                    NeighborhoodHeuristic.OROPT,
                ],
            ).getRoute()
            heuristic = "TabuSearch"
        case "SimulatedAnnealing":
            route: Route = SimulatedAnnealing(
                nodes,
                lower_bound,
                InitialSolutionHeuristics.NEARESTNEIGHBOR,
                [
                    NeighborhoodHeuristic.SWAP,
                    NeighborhoodHeuristic.TWOOPT,
                    NeighborhoodHeuristic.OROPT,
                ],
                1000,
                0.96,
            ).getRoute()
            heuristic = "SimulatedAnnealing"
        case "GeneticAlgorithm":
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
            heuristic = "GeneticAlgorithm"

    time1 = time()
    _time = time1 - time0
    times.append(_time)
    _cost = route.getCost()
    costs.append(_cost)

    graph: Graph = Graph()
    if round(route.getCost(), 2) != round(route.calculateTotalCost(graph), 2):
        raise Exception("Cost is not equal to calculateTotalCost")
    if len(route._route) != len(nodes) + 1:
        raise Exception("Route is not equal to nodes")

print(heuristic)
print(path)
print(f"Tempo mínimo de execução: {min(times)}...")
print(f"Tempo médio de execução: {statistics.mean(times)}...")
print(f"Tempo máximo de execução: {max(times)}...")
print(f"Tempo desvio padrão de execução: {statistics.stdev(times)}...")
print(f"Custo mínimo do custo: {min(costs)}...")
print(f"Custo médio do custo: {statistics.mean(costs)}...")
print(f"Custo máximo do custo: {max(costs)}...")
print(f"Custo desvio padrão do custo: {statistics.stdev(costs)}...")
print(f"Tempo {times}")
print(f"Custo {costs}")
