from random import randint
from typing import List
from ...Model.node import Node
from ...Model.route import Route
from ...Model.heuristics import *

class TabuSearch:
    def __init__(self, nodes: List[Node], lower_bound: float, tabu_list_size: int, max_iterations: int):
        self._tabu_list = []
        self._tabu_list_size = tabu_list_size
        self._max_iterations = max_iterations
        self._iteration = 0
        self._lower_bound = lower_bound

        self.route: Route

        # self.RandIns(nodes)
        # self.NearestNeighbor(nodes) 

        return self.tabuSearch()

    def tabuSearch(self) -> Route:
        while self.isStop():
            i = randint(1, len(self.route) - 1 - 1) 
            j = randint(i + 1, len(self.route) - 1 - 1)
            s = randint(0, min(2, abs(j - (i + 2))))

            move = Moves(randint(0, 2))

            self._iteration += 1

            if (i, j, move) in self._tabu_list:
                continue

            candidate_route = Route() 

            # Pesquisa do custo
            match move:
                case Moves.SWAP: 
                    candidate_route._cost = SwapCalculateCost(self.route.copy(), i, j)
                case Moves.TWOOPT: 
                    candidate_route._cost = TwoOPTCalculateCost(self.route.copy(), i, j)
                case Moves.OROPT:
                    candidate_route._cost = OrOPTCalculateCost(self.route.copy(), i, j, s)
            
            if candidate_route.getCost() > self.route.getCost():
                self._tabu_list.append(i, j, move)
                continue
            
            # Mudanca de rota
            match move:
                case Moves.SWAP: 
                    candidate_route._route = SwapCalculateRoute(self.route.copy(), i, j)
                case Moves.TWOOPT: 
                    candidate_route._route = TwoOPTCalculateRoute(self.route.copy(), i, j)
                case Moves.OROPT:
                    candidate_route._route = OrOPTCalculateRoute(self.route.copy(), i, j, s)

            self.route._route = candidate_route._route
            self._tabu_list = []
            self._iteration = 0
        
        return self.route
    
    def isStop(self) -> bool:
        return self._iteration > self._max_iterations
        return self.route.getCost() <= self._lower_bound * 1.05
    
        if self.route.getCost() <= self._lower_bound * 1.05:
            return self._iteration > self._max_iterations
        
        return False

class Moves(Enum):
    SWAP = 0
    TWOOPT = 1
    OROPT = 2