from random import randint
from typing import List
from ...Model.node import Node
from ...Model.route import Route
from ...Model.heuristics import *

class TabuSearch:
    def __init__(self, nodes: List[Node], tabu_list_size: int, max_iterations: int):
        self._tabu_list = []
        self._tabu_list_size = tabu_list_size
        self._max_iterations = max_iterations
        self._iteration = 0

        self.route: Route

        # self.RandIns(nodes)
        # self.NearestNeighbor(nodes) 

        return self.tabuSearch()

    def tabuSearch(self) -> Route:
        while self.isStop():
            i = randint(1, len(self.route) - 1 - 1) 
            j = randint(i + 1, len(self.route) - 1 - 1)
            move = Moves(randint(0, 2))
            candidate_route: Route 

            self._iteration += 1

            if (i, j, move) in self._tabu_list:
                continue

            match move:
                case Moves.SWAP: 
                    candidate_route = Swap(self.route, i, j)
                case Moves.TWOOPT: 
                    candidate_route = TwoOPT(self.route, i, j)
                case Moves.OROPT:
                    # candidate_route = OrOPT(self.route, i, j, 1)
                    # candidate_route = OrOPT(self.route, i, j, 2)
                    # candidate_route = OrOPT(self.route, i, j, 3)
                    candidate_route = OrOPT(self.route, i, j, randint(1, j - 1))
            
            if candidate_route.getCost() < self.route.getCost():
                self.route = candidate_route
                self._iteration = 0
                continue
            
            self._tabu_list.append(i, j, move)
        
        return self.route
    
    def isStop(self) -> bool:
        return self._iteration > self._max_iterations

class Moves(Enum):
    SWAP = 0
    TWOOPT = 1
    OROPT = 2