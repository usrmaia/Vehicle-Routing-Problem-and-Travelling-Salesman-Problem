from copy import copy
from typing import List
from time import time
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
).getDataFrame()
time1 = time()
print(f"Tempo de leitura do arquivo: {time1 - time0}...")
print(f"lower_bound = {lower_bound}")

time0 = time()
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
time1 = time()
print(f"Tempo de tabu dos nós: {time1 - time0}")
print(route.getCost())

# showSolution(route)
