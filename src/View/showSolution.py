from Model.graph import Graph
import networkx as nx
import matplotlib.pyplot as plt


class ShowSolution:
    def __init__(self, graph: Graph):
        self.graph = graph.graph
        node_positions = nx.get_node_attributes(graph.graph, "pos")
        plt.figure(figsize=(10, 10))
        nx.draw(
            self.graph,
            with_labels=True,
            node_size=5,
            node_color="skyblue",
            font_size=10,
            font_weight="bold",
        )
        plt.show()
