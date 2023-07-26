import time
from View.inputDataFrame import DataFrame


instance_path = "C:\\Users\\georg\\Codes\\vrp\\Data Set\\DIMACS-TSPLIB-Benchmark\\my10.tsp"
time0 = time.time()
ds_reader = DataFrame(instance_path)
ds_reader._readDataSet()
time1 = time.time()
print(f"Tempo de leitura do arquivo: {time1 - time0}")
