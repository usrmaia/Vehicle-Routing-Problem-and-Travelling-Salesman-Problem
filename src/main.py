from time import time
from Model.route import Route
from View.inputDataFrame import DataFrame
from tabuSearch import tabu_search_vrp


instance_path = "C:\\Users\\georg\\Codes\\Vehicle Routing Problem and Travelling Salesman Problem\\Data Set\\DIMACS-TSPLIB-Benchmark\\my10.tsp"

time0 = time()
ds_reader = DataFrame(instance_path)
ds_reader._readDataSet()
time1 = time()
print(f"Tempo de leitura do arquivo: {time1 - time0}")

nodes = ds_reader.getNodes()

route = tabu_search_vrp(nodes, 16, 20)
print(route)
