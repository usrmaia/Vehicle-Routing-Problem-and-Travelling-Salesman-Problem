from random import randint
from typing import List
from ...Model.node import Node
from ...Model.route import Route
from ...Model.heuristics import *

class TabuSearch:
    def __init__(self, nodes: List[Node], lower_bound: float, tabu_list_size: int, max_iterations: int):
        self._tabu_list = TabuList(tabu_list_size)
        self._max_iterations = max_iterations
        self._iteration = 0
        self._lower_bound = lower_bound

        self.route: Route

        # self.RandIns(nodes)
        self.route = NearestNeighbor(nodes) 

        self.tabuSearch()

    def tabuSearch(self) -> Route:
        while self.isStop():
            i = randint(1, len(self.route) - 1 - 1 - 1) 
            j = randint(i + 1, len(self.route) - 1 - 1)
            s = randint(0, min(2, j - i))

            _heuristic = Heuristic(randint(0, 2))

            self._iteration += 1

            if (i, j, s, _heuristic) in self._tabu_list:
                continue

            candidate_route = Route() 

            # Pesquisa do custo
            match _heuristic:
                case Heuristic.SWAP: 
                    candidate_route._cost = SwapCalculateCost(self.route.copy(), i, j)
                case Heuristic.TWOOPT: 
                    candidate_route._cost = TwoOPTCalculateCost(self.route.copy(), i, j)
                case Heuristic.OROPT:
                    candidate_route._cost = OrOPTCalculateCost(self.route.copy(), i, j, s)
            
            if candidate_route.getCost() > self.route.getCost():
                self._tabu_list.append(i, j, move)
                continue
            
            # Mudanca de rota
            match _heuristic:
                case Heuristic.SWAP: 
                    candidate_route._route = SwapCalculateRoute(self.route.copy(), i, j)
                case Heuristic.TWOOPT: 
                    candidate_route._route = TwoOPTCalculateRoute(self.route.copy(), i, j)
                case Heuristic.OROPT:
                    candidate_route._route = OrOPTCalculateRoute(self.route.copy(), i, j, s)

            self.route._route = candidate_route._route
            self._iteration = 0
        
        return self.route
    
    def isStop(self) -> bool:
        return self._iteration > self._max_iterations
        return self.route.getCost() <= self._lower_bound * 1.05
    
        if self.route.getCost() <= self._lower_bound * 1.05:
            return self._iteration > self._max_iterations
        
        return False

    def getRoute(self) -> Route:
        return self.route

class Heuristic(Enum):
    SWAP = 0
    TWOOPT = 1
    OROPT = 2

class TabuList:
    def __init__(self, len) -> None:
        self._tabu_list = {}
        self._len = len
    
    def append(self, move):
        if len(self._tabu_list) > self._len:
            self._tabu_list = {}

        self._tabu_list[move] = True
    
    def __contains__(self, move):
        return move in self._tabu_list
