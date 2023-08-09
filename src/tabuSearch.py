from random import randint
from typing import List
from enum import Enum
from node import Node
from route import Route
from heuristics import *


class TabuSearch:
    def __init__(
        self,
        nodes: List[Node],
        intance_lower_bound: float,
        tabu_list_size: int,
        max_iterations: int,
    ):
        self._tabu_list = TabuList(tabu_list_size)

        self._iteration = 0
        self._max_iteration = max_iterations

        self.intance_lower_bound = intance_lower_bound

        self.best_route: Route()
        

        # self.best_route = self.RandIns(nodes)
        self.best_route = NearestNeighbor(nodes)

        # free nodes

        self.tabuSearch()

    def tabuSearch(self):
        while not self.isStop():
            i = randint(1, len(self.best_route) - 1 - 1 - 1)
            j = randint(i + 1, len(self.best_route) - 1 - 1)
            segment = randint(0, min(2, j - i))

            heuristic = Heuristic(randint(0, 2))
            move = Move(heuristic, i, j, segment)

            self._iteration += 1

            if move in self._tabu_list:
                continue

            candidate_route = Route()

            # Pesquisa do custo
            match heuristic:
                case Heuristic.SWAP:
                    candidate_route._cost = SwapCalculateCost(self.best_route.copy(), i, j)
                case Heuristic.TWOOPT:
                    candidate_route._cost = TwoOPTCalculateCost(self.best_route.copy(), i, j)
                case Heuristic.OROPT:
                    candidate_route._cost = OrOPTCalculateCost(
                        self.best_route.copy(), i, j, segment
                    )

            if candidate_route.getCost() > self.best_route.getCost():
                self._tabu_list.append(move)
                continue

            # Mudanca de rota
            match heuristic:
                case Heuristic.SWAP:
                    candidate_route._route = SwapCalculateRoute(self.best_route.copy(), i, j)
                case Heuristic.TWOOPT:
                    candidate_route._route = TwoOPTCalculateRoute(
                        self.best_route.copy(), i, j
                    )
                case Heuristic.OROPT:
                    candidate_route._route = OrOPTCalculateRoute(
                        self.best_route.copy(), i, j, segment
                    )

            self.best_route = candidate_route
            self._iteration = 0

    def isStop(self) -> bool:
        return self._iteration > self._max_iteration
        # return self.best_route.getCost() <= self._lower_bound * 1.05

        # if self.best_route.getCost() <= self._lower_bound * 1.05:
        #     return self._iteration > self._max_iterations

        # return False

    def getRoute(self) -> Route:
        self.best_route.calculateTotalCost()

        return self.best_route


class Heuristic(Enum):
    SWAP = 0
    TWOOPT = 1
    OROPT = 2

class Move:
    def __init__(self, heuristic, i, j, segment=None) -> None:
        self.heuristic = heuristic
        self.i = i
        self.j = j
        self.segment = segment


class TabuList:
    def __init__(self, len) -> None:
        self._tabu_list = {}
        self._len = len

    def append(self, move: Move):
        # Manutenção do tamanho da lista
        if len(self._tabu_list) > self._len:
            self._tabu_list.clear() # Abordagem que limpa a lista
            # self._tabu_list.pop(self._tabu_list.values()[0]) # Abordagem que remove o primeiro elemento

        if move.heuristic != Heuristic.OROPT:
            move = Move(move.heuristic, move.i, move.j)

        self._tabu_list[move] = True 
        

    def __contains__(self, move: Move):
        if move.heuristic == Heuristic.OROPT:
            return move in self._tabu_list
        
        return (move.heuristic, move.i, move.j) in self._tabu_list