import numpy as np


class Graph:
    def __init__(self, parsed_data):
        self.X = parsed_data["x"] + 1
        self.Y = parsed_data["y"] + 1
        self.packages = parsed_data["packages"]
        self.special_edges = parsed_data["special_edges"]
        self.agents = parsed_data["agents"]

        self.total_nodes = self.X * self.Y
        self.adjacency_matrix = None
        self._build_adjacency_matrix()

    def _coordinate_to_index(self, row, col):
        if row < 0 or row >= self.X or col < 0 or col >= self.Y:
            raise ValueError("Adjacency Matrix out of bounds")
        return row * self.Y + col

    def _build_adjacency_matrix(self):
        self.adjacency_matrix = np.zeros(shape=(self.total_nodes, self.total_nodes), dtype=int)

        for i in range(self.X):
            for j in range(self.Y):
                current_node = self._coordinate_to_index(i, j)

                # Connect with the right neighbor (if exists)
                if j + 1 < self.Y:
                    right_neighbor = self._coordinate_to_index(i, j + 1)
                    self.adjacency_matrix[current_node, right_neighbor] = 1
                    self.adjacency_matrix[right_neighbor, current_node] = 1

                # Connect with the bottom neighbor (if exists)
                if i + 1 < self.X:
                    bottom_neighbor = self._coordinate_to_index(i + 1, j)
                    self.adjacency_matrix[current_node, bottom_neighbor] = 1
                    self.adjacency_matrix[bottom_neighbor, current_node] = 1

        self.apply_special_edges()

    def apply_special_edges(self):
        for special_edge in self.special_edges:
            if special_edge["type"] == "always blocked":
                first_node = self._coordinate_to_index(special_edge["from"][0], special_edge["from"][1])
                second_node = self._coordinate_to_index(special_edge["to"][0], special_edge["to"][1])

                self.adjacency_matrix[first_node, second_node] = 0
                self.adjacency_matrix[second_node, first_node] = 0

    def update_state(self, state):
        self.packages = state["packages"]
        self.special_edges = state["special_edges"]
        self.agents = state["agents"]
