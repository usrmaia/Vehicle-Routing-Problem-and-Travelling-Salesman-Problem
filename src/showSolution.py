import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from node import Node
from route import Route


def showSolution(route: Route):
    G = nx.DiGraph()

    for i, n in enumerate(route._route):
        if i < len(route._route) - 1:
            G.add_edge(
                (n.coord_x, n.coord_y),
                (route._route[i + 1].coord_x, route._route[i + 1].coord_y),
                weight=n.distanceTo(route._route[i + 1]),
            )

    node_positions = {
        (n.coord_x, n.coord_y): (n.coord_x, n.coord_y) for n in route._route
    }

    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    nx.draw(G, pos=node_positions, ax=ax, node_size=5, with_labels=False)

    nx.draw_networkx_nodes(
        G,
        pos=node_positions,
        ax=ax,
        nodelist=[(route._route[0].coord_x, route._route[0].coord_y)],
        node_size=10,
        node_color="red",
    )  # Primeiro nó em vermelho

    node_labels = {
        (node.coord_x, node.coord_y): (node.coord_x, node.coord_y)
        for node in route._route
    }

    nx.draw_networkx_labels(
        G,
        pos=node_positions,
        labels=node_labels,
        font_size=10,
        font_color="black",
        verticalalignment="top",
        horizontalalignment="left",
    )  # "bottom" para abaixo

    edge_labels = {
        (edge[0], edge[1]): f'{G.get_edge_data(*edge)["weight"]:.2f}'
        for edge in G.edges
    }
    nx.draw_networkx_edge_labels(
        G,
        pos=node_positions,
        edge_labels=edge_labels,
        font_size=8,
        font_color="black",
    )

    ax.set_xlim(-2, 12)
    ax.set_ylim(-2, 12)

    plt.show()
