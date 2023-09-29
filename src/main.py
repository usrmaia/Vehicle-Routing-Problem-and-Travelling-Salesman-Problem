from copy import copy
from random import seed
from typing import List
from time import time
from geneticAlgorithm import GeneticAlgorithm
from simulatedAnnealing import SimulatedAnnealing
from tabuSearch import TabuSearch
from heuristics import *
from route import Route
from node import Node
from inputDataFrame import DataFrame

# from showSolution import showSolution

time0 = time()
nodes: List[Node]
nodes, lower_bound = DataFrame(
    # "C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\vm1084.tsp"
    "C:\\Users\\konstroi.dev\\Codes\\Vehicle-Routing-Problem-and-Travelling-Salesman-Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\vm1084.tsp"
    # "/workspaces/Vehicle-Routing-Problem-and-Travelling-Salesman-Problem/Data Set/DIMACS-TSPLIB-Benchmark/my10.tsp"
    # "C:\\Users\\konstroi.dev\\Codes\\Vehicle-Routing-Problem-and-Travelling-Salesman-Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\my10.tsp"
).getDataFrame()
time1 = time()
print(f"Tempo de leitura do arquivo: {time1 - time0}...")
print(f"lower_bound = {lower_bound}")

time0 = time()
"""
route: Route = TabuSearch(
    nodes,
    lower_bound,
    50,
    4000 + 40 * len(nodes),
    InitialSolutionHeuristics.NEARESTNEIGHBOR,
    [
        NeighborhoodHeuristic.SWAP,
        NeighborhoodHeuristic.TWOOPT,
        NeighborhoodHeuristic.OROPT,
    ],
).getRoute()
"""
"""
route: Route = SimulatedAnnealing(
    nodes,
    lower_bound,
    1000,
    InitialSolutionHeuristics.NEARESTNEIGHBOR,
    [
        NeighborhoodHeuristic.SWAP,
        NeighborhoodHeuristic.TWOOPT,
        NeighborhoodHeuristic.OROPT,
    ],
    100,
    0.7,
).getRoute()
"""
# seed(42)
route: Route = GeneticAlgorithm(
    nodes=nodes,
    intance_lower_bound=lower_bound,
    initial_solution_heuristic=InitialSolutionHeuristics.RANDOMINSERTION,
    neighborhood_heuristics=[
        NeighborhoodHeuristic.SWAP,
        NeighborhoodHeuristic.TWOOPT,
        NeighborhoodHeuristic.OROPT,
    ],
    max_generations=1,
    population_size=5,
    crossover_probability=50,
    mutation_probability=70,
    elitis=20,
    max_time=100,
).getRoute()
time1 = time()
print(f"Tempo de tabu dos nós: {time1 - time0}")
print(route.getCost())
graph: Graph = Graph()
if round(route.getCost(), 2) != round(route.calculateTotalCost(graph), 2):
    raise Exception("Cost is not equal to calculateTotalCost")
if len(route._route) != len(nodes) + 1:
    raise Exception("Route is not equal to nodes")
print("ok")

# showSolution(route)
