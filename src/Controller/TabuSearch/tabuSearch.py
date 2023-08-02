from random import randint
from typing import List
from ...Model.node import Node
from ...Model.route import Route


def tabu_search_vrp(nodes: list[Node], tabu_size: int, max_iterations: int) -> Route:
    # Initialize a solution with random routes for each vehicle
    initial_solution = Route()

    depot = nodes.pop(0)
    initial_solution.setNode(depot, 0)

    len_route = len(nodes)

    while len(nodes):
        n = randint(0, len(nodes) - 1)
        node = nodes.pop(n)

        initial_solution.setNode(node, node.distanceTo(depot))

    # Tabu search variables
    best_solution = initial_solution
    best_cost = best_solution.getCost()
    tabu_list = []
    iteration = 0

    while iteration < max_iterations:
        candidate_solutions: List[Route] = []
        candidate_solution = best_solution

        for k in range(1, len_route - 1):
            for l in range(1, len_route - 1):
                move = (k, l)

                iteration += 1
                if move in tabu_list:
                    iteration += 1
                    continue

                candidate_solution = doMove(candidate_solution, k, l)

                # Add the move to the tabu list
                tabu_list.append(move)

                if len(tabu_list) > tabu_size:
                    tabu_list.pop(0)

                candidate_solutions.append(candidate_solution)

        # Choose the best candidate solution
        candidate_solutions.sort(key=lambda r: r.getCost())
        best_candidate = candidate_solutions[0]

        if best_candidate.getCost() < best_cost:
            best_solution = best_candidate
            best_cost = best_candidate.getCost()
            iteration = 0

    return best_solution


def doMove(route: Route, i: int, j: int) -> Route:
    node_aux: Node = route._route[i]
    route._route[i] = route._route[j]
    route._route[j] = node_aux

    return route


class TabuSearch:
    def __init__(self, nodes: List[Node], tabu_list_size: int, max_iterations: int):
        self._tabu_list = []
        self._tabu_list_size = tabu_list_size
        self._max_iterations = max_iterations

        self.route: Route

        # self.RandIns(nodes)
        # self.NearestNeighbor(nodes)

    def RandIns(self, nodes: List[Node]):
        depot = nodes.pop[0]
        self.route.setNode(depot)

        while len(nodes):
            node = nodes.pop(randint(0, len(nodes) - 1))
            self.route.setNode(node)

        self.route.setNode(depot)
        self.route.calculateTotalCost()

    def NearestNeighbor(self, nodes: List[Node]):
        depot = nodes.pop[0]
        self.route.setNode(depot)
        # Adiciona um nó aleatório após o depot para iniciar o NN
        self.route.setNode(nodes.pop(randint(0, len(nodes) - 1)))

        while len(nodes):
            nearest_node = min(nodes, key=lambda n: n.distanceTo(self.route[-1]))
            self.route.setNode(nearest_node)
            nodes.remove(nearest_node)

        self.route.setNode(depot)
        self.route.calculateTotalCost()

    def Swap(self, i, j):
        self.route.unsetCost(self.route._route[i].distanceTo(self.route._route[i + 1]))
        self.route.unsetCost(self.route._route[i-1].distanceTo(self.route._route[i]))
        self.route.unsetCost(self.route._route[j].distanceTo(self.route._route[j+1]))
        self.route.unsetCost(self.route._route[j-1].distanceTo(self.route._route[j]))

        self.route._route[i], self.route._route[j] = (
            self.route._route[j],
            self.route._route[i],
        )

        self.route.setCost(self.route._route[i].distanceTo(self.route._route[i + 1]))
        self.route.setCost(self.route._route[i-1].distanceTo(self.route._route[i]))
        self.route.setCost(self.route._route[j].distanceTo(self.route._route[j+1]))
        self.route.setCost(self.route._route[j-1].distanceTo(self.route._route[j]))

    def TwoOPT(self, i, j):
        self.route.unsetCost(self.route._route[i].distanceTo(self.route._route[i + 1]))
        self.route.unsetCost(self.route._route[j - 1].distanceTo(self.route._route[j]))

        self.route._route = (
            self.route._route[: i + 1]
            + self.route._route[j:i:-1]
            + self.route._route[j + 1 :]
        )

        self.route.setCost(self.route._route[i].distanceTo(self.route._route[i + 1]))
        self.route.setCost(self.route._route[j - 1].distanceTo(self.route._route[j]))

    def OrOPT1(self, i, j):
        self.route.unsetCost(self.route._route[i].distanceTo(self.route._route[i + 1]))
        self.route.unsetCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.unsetCost(self.route._route[j].distanceTo(self.route._route[j + 1]))

        self.route._route = (
            self.route._route[:i]
            + self.route._route[i + 1 : j]
            + self.route._route[i : i + 1]
            + self.route._route[j :]
        )

        self.route.setCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.setCost(self.route._route[j].distanceTo(self.route._route[j + 1]))
        self.route.setCost(self.route._route[j - 1].distanceTo(self.route._route[j]))

    def OrOPT2(self, i, j):
        self.route.unsetCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.unsetCost(self.route._route[i + 1].distanceTo(self.route._route[i + 2]))
        self.route.unsetCost(self.route._route[j + 1].distanceTo(self.route._route[j + 2]))

        self.route._route = (
            self.route._route[:i]
            + self.route._route[i + 2 : j]
            + self.route._route[i : i + 1]
            + self.route._route[j :]
        )

        self.route.setCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.setCost(self.route._route[i + 1].distanceTo(self.route._route[i + 2]))
        self.route.setCost(self.route._route[j + 1].distanceTo(self.route._route[j + 2]))
    
    def OrOPT3(self, i, j):
        self.route.unsetCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.unsetCost(self.route._route[i + 2].distanceTo(self.route._route[i + 3]))
        self.route.unsetCost(self.route._route[j + 1].distanceTo(self.route._route[j + 2]))

        self.route._route = (
            self.route._route[:i]
            + self.route._route[i + 3 : j]
            + self.route._route[i : i + 3]
            + self.route._route[j :]
        )

        self.route.setCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.setCost(self.route._route[i + 2].distanceTo(self.route._route[i + 3]))
        self.route.setCost(self.route._route[j + 1].distanceTo(self.route._route[j + 2]))
    
    def OrOPT(self, i, j, segment):
        self.route.unsetCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.unsetCost(self.route._route[i + segment].distanceTo(self.route._route[i + segment + 1]))
        self.route.unsetCost(self.route._route[j].distanceTo(self.route._route[j + 1]))

        self.route._route = (
            self.route._route[:i]
            + self.route._route[i + segment : j]
            + self.route._route[i : i + segment]
            + self.route._route[j :]
        )

        self.route.setCost(self.route._route[i - 1].distanceTo(self.route._route[i]))
        self.route.setCost(self.route._route[i + segment].distanceTo(self.route._route[i + segment + 1]))
        self.route.setCost(self.route._route[j].distanceTo(self.route._route[j + 1]))

        