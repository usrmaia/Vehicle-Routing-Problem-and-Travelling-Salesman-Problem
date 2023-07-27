from io import TextIOWrapper
from Model.node import Node


class DataFrame:
    def __init__(self, path):
        self.path = path
        self.nodes: list[Node] = []

        self._readDataSet()

    def _readDataSet(self):
        with open(self.path, "r") as lines:
            for line in lines:
                if not line.startswith("NODE_COORD_SECTION"):
                    continue

                next(lines)
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

    def getNodes(self) -> list[Node]:
        return self.nodes
