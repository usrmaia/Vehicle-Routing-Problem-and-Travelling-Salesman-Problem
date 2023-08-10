from copy import copy
from typing import List
from time import time
from tabuSearch import TabuSearch
from route import Route
from node import Node
from inputDataFrame import DataFrame
from showSolution import showSolution

time0 = time()
nodes: List[Node]
nodes, lower_bound = DataFrame(
    "C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\pla85900.tsp"
).getDataFrame()
time1 = time()
print(f"Tempo de leitura do arquivo: {time1 - time0}...")
print(f"lower_bound = {lower_bound}")

time0 = time()
route: Route = TabuSearch(nodes, lower_bound, 500, 4000 + 40 * len(nodes)).getRoute()
time1 = time()
print(f"Tempo de tabu dos nós: {time1 - time0}")

print(route)

# showSolution(route)
