from typing import List
from io import TextIOWrapper
from node import Node


class DataFrame:
    def __init__(self, path) -> None:
        self.path = path
        self.nodes: List[Node] = []
        self.lowerBound = -1

        self._readDataSet()

    def _readDataSet(self):
        with open(self.path, "r") as lines:
            for line in lines:
                if line.startswith("LOWER_BOUND"):
                    self.lowerBound = float(line.split()[2])
                    continue

                if not line.startswith("NODE_COORD_SECTION"):
                    continue

                self._buildDataList(lines)
                break

    def _buildDataList(self, lines: TextIOWrapper):
        for line in lines:
            if line.strip() == "EOF":
                break

            node_data = line.split()
            node_data = self.nodes.append(
                Node(int(node_data[0]), float(node_data[1]), float(node_data[2]))
            )

    def getDataFrame(self) -> tuple[List[Node], float]:
        return self.nodes, self.lowerBound
