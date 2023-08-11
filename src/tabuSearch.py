from sys import maxsize
from random import randint, seed, choice, randrange
from copy import copy
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
        # seed(42)
        self._tabu_list = TabuList(tabu_list_size)

        self._iteration = 0
        self._max_iteration = max_iterations

        self.intance_lower_bound = intance_lower_bound

        self.best_route = Route()
        self.nodes = nodes

        # self.best_route = RandomInsertion(nodes)
        self.best_route = NearestNeighbor(copy(nodes))

        # free nodes

        # self.tabuSearch()
        self.tabuSearchLS()

    def tabuSearch(self):
        # seed(42)
        while not self.isStop():
            i = randint(1, len(self.best_route._route) - 1 - 1 - 1)
            j = randint(i + 1, len(self.best_route._route) - 1 - 1)
            segment = randint(0, min(2, j - i - 1))

            heuristic = Heuristic(randint(0, 2))
            move = Move(heuristic, i, j, segment)

            self._iteration += 1

            if move in self._tabu_list:
                continue

            candidate_route = copy(self.best_route)

            # Pesquisa do custo
            match heuristic:
                case Heuristic.SWAP:
                    SwapCalculateCost(candidate_route, i, j)
                case Heuristic.TWOOPT:
                    TwoOPTCalculateCost(candidate_route, i, j)
                case Heuristic.OROPT:
                    OrOPTCalculateCost(candidate_route, i, j, segment)

            if candidate_route.getCost() > self.best_route.getCost():
                self._tabu_list.append(move)
                continue

            # Mudanca de rota
            match heuristic:
                case Heuristic.SWAP:
                    SwapCalculateRoute(candidate_route, i, j)
                case Heuristic.TWOOPT:
                    TwoOPTCalculateRoute(candidate_route, i, j)
                case Heuristic.OROPT:
                    OrOPTCalculateRoute(candidate_route, i, j, segment)

            self.best_route = copy(candidate_route)
            self._iteration = 0

    def tabuSearchFor(self):
        # seed(42)
        while not self.isStop():
            for i in range(1, len(self.best_route._route) - 1 - 1 - 1):
                for j in range(i + 1, len(self.best_route._route) - 1 - 1):
                    for heuristic in range(0, 2):
                        heuristic = Heuristic(heuristic)
                        segment = randint(0, min(2, j - i - 1))

                        # heuristic = Heuristic(randint(0, 2))
                        move = Move(heuristic, i, j, segment)

                        self._iteration += 1

                        if move in self._tabu_list:
                            continue

                        candidate_route = copy(self.best_route)

                        # Pesquisa do custo
                        match heuristic:
                            case Heuristic.SWAP:
                                SwapCalculateCost(candidate_route, i, j)
                            case Heuristic.TWOOPT:
                                TwoOPTCalculateCost(candidate_route, i, j)
                            case Heuristic.OROPT:
                                OrOPTCalculateCost(candidate_route, i, j, segment)

                        if candidate_route.getCost() > self.best_route.getCost():
                            self._tabu_list.append(move)
                            continue

                        # Mudanca de rota
                        match heuristic:
                            case Heuristic.SWAP:
                                SwapCalculateRoute(candidate_route, i, j)
                            case Heuristic.TWOOPT:
                                TwoOPTCalculateRoute(candidate_route, i, j)
                            case Heuristic.OROPT:
                                OrOPTCalculateRoute(candidate_route, i, j, segment)

                        self.best_route = copy(candidate_route)
                        self._iteration = 0

    def tabuSearchN(self):
        # seed(42)
        candidate_routes = self.neighborhood(
            self.best_route, 10, self.best_route.getCost()
        )
        c_s, c_t, c_o = 0, 0, 0
        while not self.isStop():
            for c, candidate_route in enumerate(candidate_routes):
                for i in range(1, len(candidate_route._route) - 1 - 1 - 1):
                    for j in range(i + 1, len(candidate_route._route) - 1 - 1):
                        for heuristic in range(0, 3):
                            heuristic = Heuristic(heuristic)
                            # segment = randint(0, min(2, j - i - 1))
                            segment = 0
                            # heuristic = Heuristic(randint(0, 2))
                            move = Move(heuristic, i, j, segment)

                            self._iteration += 1

                            if move in self._tabu_list:
                                continue

                            temp_candidate_route = copy(candidate_route)

                            # Pesquisa do custo
                            match heuristic:
                                case Heuristic.SWAP:
                                    SwapCalculateCost(temp_candidate_route, i, j)
                                case Heuristic.TWOOPT:
                                    TwoOPTCalculateCost(temp_candidate_route, i, j)
                                case Heuristic.OROPT:
                                    OrOPTCalculateCost(
                                        temp_candidate_route, i, j, segment
                                    )

                            if (
                                temp_candidate_route.getCost()
                                > candidate_route.getCost()
                            ):
                                self._tabu_list.append(move)
                                continue

                            # Mudanca de rota
                            match heuristic:
                                case Heuristic.SWAP:
                                    SwapCalculateRoute(temp_candidate_route, i, j)
                                    c_s += 1
                                case Heuristic.TWOOPT:
                                    TwoOPTCalculateRoute(temp_candidate_route, i, j)
                                    c_t += 1
                                case Heuristic.OROPT:
                                    OrOPTCalculateRoute(
                                        temp_candidate_route, i, j, segment
                                    )
                                    c_o += 1

                            candidate_routes[c] = copy(temp_candidate_route)
                            self._iteration = 0

        self.best_route = min(enumerate(candidate_routes), key=lambda n: n[i].getCost())
        print(c_s, c_t, c_o)

    def tabuSearchLS(self):
        candidate_routes = self.neighborhood(
            self.best_route, 10, self.best_route.getCost()
        )

        c_t = 0
        for candidate_index, candidate_route in enumerate(candidate_routes):
            while not self.isStop():
                for i in range(1, len(candidate_route._route) - 1 - 1): 
                    j = randint(1, len(candidate_route._route) - 1 - 1)

                    if i == j:
                        continue

                    # heuristics = [Heuristic.SWAP, Heuristic.TWOOPT, Heuristic.OROPT]
                    heuristics = [Heuristic.TWOOPT]

                    while heuristics:
                        heuristic = heuristics.pop(randrange(len(heuristics)))

                        self._iteration += 1

                        # verificar se é tabu

                        node_i, node_j = i, j
                        if not heuristic.OROPT and j < i:
                            node_i, node_j = j, i

                        # Pesquisa do custo
                        match heuristic:
                            case Heuristic.SWAP:
                                cost = SwapCalculateCost(copy(candidate_route), node_i, node_j)
                            case Heuristic.TWOOPT:
                                cost = TwoOPTCalculateCost(copy(candidate_route), node_i, node_j)
                            case Heuristic.OROPT:
                                cost = OrOPTCalculateCost(copy(candidate_route), node_i, node_j)

                        # if neighbor_route.getCost() > limit:
                        if cost > candidate_route.getCost():
                            # self._tabu_list.append(move)
                            # adicionar rota a lista tabu
                            continue

                        # Atualização do custo
                        candidate_route._cost = cost

                        # Mudanca de rota
                        route = List[Node]
                        match heuristic:
                            case Heuristic.SWAP:
                                candidate_route = SwapCalculateRoute(copy(candidate_route), node_i, node_j)
                            case Heuristic.TWOOPT:
                                route = TwoOPTCalculateRoute(copy(candidate_route), node_i, node_j)
                                c_t += 1
                            case Heuristic.OROPT:
                                candidate_route = OrOPTCalculateRoute(copy(candidate_route), node_i, node_j)
                        
                        candidate_route._route = route
                        
                        self._iteration = 0
                    
        self.best_route = min(enumerate(candidate_routes), key=lambda n: n[1].getCost())
        # self.best_route = candidate_route
        print(c_t)

    def neighborhood(
        self, route: Route, qtd_candidates: int, limit=maxsize
    ) -> List[Route]:
        candidate_routes: List[Route] = [route] * qtd_candidates
        qtd_de_melhorias = [0] * qtd_candidates

        for candidate_index, candidate_route in enumerate(candidate_routes):
            for i in range(1, len(candidate_route._route) - 1):
                j = randint(1, len(candidate_route._route) - 1 - 1)

                if i == j:
                    continue

                heuristics = [Heuristic.SWAP, Heuristic.TWOOPT, Heuristic.OROPT]

                while heuristics:
                    heuristic = heuristics.pop(randrange(len(heuristics)))

                    # verificar se é tabu

                    node_i, node_j = i, j
                    if not heuristic.OROPT and j < i:
                        node_i, node_j = j, i

                    cost = maxsize

                    neighbor_route = copy(candidate_route)

                    # Pesquisa do custo
                    match heuristic:
                        case Heuristic.SWAP:
                            cost = SwapCalculateCost(copy(neighbor_route), node_i, node_j)
                        case Heuristic.TWOOPT:
                            cost = TwoOPTCalculateCost(copy(neighbor_route), node_i, node_j)
                        case Heuristic.OROPT:
                            cost = OrOPTCalculateCost(copy(neighbor_route), node_i, node_j)

                    # if neighbor_route.getCost() > limit:
                    if cost > candidate_route.getCost():
                        # self._tabu_list.append(move)
                        # adicionar rota a lista tabu
                        continue

                    # Atualização do custo
                    candidate_route._cost = cost

                    rroute = Route()

                    # Mudanca de rota
                    match heuristic:
                        case Heuristic.SWAP:
                            rroute = SwapCalculateRoute(copy(candidate_route), node_i, node_j)
                            qtd_de_melhorias[candidate_index] += 1
                        case Heuristic.TWOOPT:
                            rroute = TwoOPTCalculateRoute(copy(candidate_route), node_i, node_j)
                            qtd_de_melhorias[candidate_index] += 1
                        case Heuristic.OROPT:
                            rroute = OrOPTCalculateRoute(copy(candidate_route), node_i, node_j)
                            qtd_de_melhorias[candidate_index] += 1
                    
                    candidate_route._route = rroute._route

        print(qtd_de_melhorias)
        return candidate_routes

    def isStop(self) -> bool:
        # return True
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
            self._tabu_list.clear()  # Abordagem que limpa a lista
            # self._tabu_list.pop(self._tabu_list.values()[0]) # Abordagem que remove o primeiro elemento

        if move.heuristic != Heuristic.OROPT:
            move = Move(move.heuristic, move.i, move.j)

        self._tabu_list[move] = True

    def __contains__(self, move: Move):
        if move.heuristic == Heuristic.OROPT:
            return move in self._tabu_list

        return (move.heuristic, move.i, move.j) in self._tabu_list
