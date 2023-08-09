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
        lower_bound: float,
        tabu_list_size: int,
        max_iterations: int,
    ):
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
            move = Move(i, j, s, _heuristic)

            self._iteration += 1

            if move in self._tabu_list:
                continue

            candidate_route = Route()

            # Pesquisa do custo
            match _heuristic:
                case Heuristic.SWAP:
                    candidate_route._cost = SwapCalculateCost(self.route.copy(), i, j)
                case Heuristic.TWOOPT:
                    candidate_route._cost = TwoOPTCalculateCost(self.route.copy(), i, j)
                case Heuristic.OROPT:
                    candidate_route._cost = OrOPTCalculateCost(
                        self.route.copy(), i, j, s
                    )

            if candidate_route.getCost() > self.route.getCost():
                self._tabu_list.append(move)
                continue

            # Mudanca de rota
            match _heuristic:
                case Heuristic.SWAP:
                    candidate_route._route = SwapCalculateRoute(self.route.copy(), i, j)
                case Heuristic.TWOOPT:
                    candidate_route._route = TwoOPTCalculateRoute(
                        self.route.copy(), i, j
                    )
                case Heuristic.OROPT:
                    candidate_route._route = OrOPTCalculateRoute(
                        self.route.copy(), i, j, s
                    )

            self.route._route = candidate_route._route
            self.route._cost = candidate_route.getCost()
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

class Move:
    def __init__(self, i, j, s, h) -> None:
        self.i = i
        self.j = j
        self.s = s
        self.h = h


class TabuList:
    def __init__(self, len) -> None:
        self._tabu_list = {}
        self._len = len

    def append(self, move: Move):
        if len(self._tabu_list) > self._len:
            self._tabu_list.clear() # Abordagem que limpa a lista
            # self._tabu_list.pop(self._tabu_list.values()[0]) # Abordagem que remove o primeiro elemento

        if move.h != Heuristic.OROPT:
            move = (move.i, move.j, move.h)

        self._tabu_list[move] = True 
        

    def __contains__(self, move: Move):
        if move.h == Heuristic.OROPT:
            return move in self._tabu_list
        
        return (move.i, move.j, move.h) in self._tabu_list