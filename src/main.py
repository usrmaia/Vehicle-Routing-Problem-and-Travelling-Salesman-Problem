from typing import List
from time import time
from Model.route import Route
from Model.node import Node
from View.inputDataFrame import DataFrame

# from Controller.TabuSearch.tabuSearch import tabu_search_vrp


time0 = time()
nodes: List[Node]
nodes, lowerBound = DataFrame(
    "C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\my10.tsp"
).getDataFrame()
time1 = time()
print(f"Tempo de leitura do arquivo: {time1 - time0}... {nodes}, {lowerBound}")

# time0 = time()
# route = tabu_search_vrp(nodes, 16, 5)
# time1 = time()
# print(f"Tempo de tabu dos nós: {time1 - time0}")

# print(route.calculateTotalCost())
