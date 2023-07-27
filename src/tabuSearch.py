from random import randint
from typing import List
from Model.node import Node
from Model.route import Route


def tabu_search_vrp(nodes: list[Node], tabu_size: int, max_iterations: int) -> Route:
    # Initialize a solution with random routes for each vehicle
    initial_solution = Route()

    depot = nodes.pop(0)
    initial_solution.setNode(depot, 0)

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
        candidate_solutions: List[Route]

        for k in range(1, len(nodes) - 1):
            for l in range(1, len(nodes) - 1):
                move = (k, l)

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

    return best_solution


def doMove(route: Route, i: int, j: int) -> Route:
    route1 = route[:i]
    route2 = route[i + 1 : j]
    route3 = route[j + 1 :]

    return route1 + route[j] + route2 + route[i] + route3
