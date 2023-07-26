import numpy as np
import networkx as nx
from .node import Vertex


class Graph:
    def __init__(self, vertices: list[Vertex]):
        self.vertices = vertices
        self.num_vertices = len(vertices)
        self.graph = nx.Graph()
        self.distances = self._calculateDistances()

    def _calculateDistances(self):
        self.distances = np.zeros((self.num_vertices, self.num_vertices))

        for i in range(self.num_vertices - 1):
            for j in range(i + 1, self.num_vertices):
                distance = self.vertices[i].distanceTo(self.vertices[j])

                self.distances[
                    self.vertices[i].id - 1, self.vertices[j].id - 1
                ] = distance
                self.distances[
                    self.vertices[j].id - 1, self.vertices[i].id - 1
                ] = distance

                self.graph.add_edge(i, j, distance=distance)

    def __str__(self) -> str:
        return f"Matriz with {self.num_vertices} vertices:\n{self.distances}"
