from Model.node import Node
from Model.route import Route
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class ShowSolution:
    def __init__(self, route: Route):
        route = Route()
        route._route = [
            Node(1, 5, 5),
            Node(2, 0, 4),
            Node(3, 2, 0),
            Node(4, 5, 1),
            Node(5, 10, 1),
            Node(6, 2, 8),
            Node(7, 6, 10),
            Node(8, 7, 7),
            Node(9, 10, 6),
            Node(10, 9, 9),
            Node(1, 5, 5),
        ]
        route.calculateTotalCost()

        self.graph = nx.Graph()

        for i, n in enumerate(route._route):
            G.add_node(n, pos=nodes[i])

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                G.add_edge(i, j, weight=route._route[i].distanceTo(j))

        node_positions = nx.get_node_attributes(G, 'pos')

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos=node_positions, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold')

        route_color = 'r'
        edges = list(zip(route._route, route._route[:]))
        nx.draw_networkx_edges(G, pos=node_positions, edgelist=edges, edge_color=route_color, width=2)

        plt.show()

ShowSolution()