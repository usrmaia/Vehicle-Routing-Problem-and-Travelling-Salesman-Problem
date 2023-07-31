from time import time
from Model.route import Route
from View.inputDataFrame import DataFrame
from Controller.TabuSearch.tabuSearch import tabu_search_vrp


instance_path = "C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\pla85900.tsp"

time0 = time()
ds_reader = DataFrame(instance_path)
time1 = time()
print(f"Tempo de leitura do arquivo: {time1 - time0}")

nodes = ds_reader.getNodes()
time0 = time()
route = tabu_search_vrp(nodes, 16, 5)
time1 = time()
print(f"Tempo de tabu dos nós: {time1 - time0}")

print(route.calculateTotalCost())
