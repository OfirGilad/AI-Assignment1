import numpy as np


class Graph:
    def __init__(self, parsed_data: dict):
        self.X = parsed_data["x"] + 1
        self.Y = parsed_data["y"] + 1
        self.packages = parsed_data.get("packages", list())
        self.special_edges = parsed_data.get("special_edges", list())
        self.agents = parsed_data.get("agents", list())

        self.total_vertices = self.X * self.Y
        self.adjacency_matrix = None
        self._build_adjacency_matrix()

    def coordinates_to_vertex_index(self, row, col):
        if row < 0 or row >= self.X or col < 0 or col >= self.Y:
            raise ValueError("Adjacency Matrix out of bounds")
        return row * self.Y + col

    def _build_adjacency_matrix(self):
        self.adjacency_matrix = np.zeros(shape=(self.total_vertices, self.total_vertices), dtype=int)

        for i in range(self.X):
            for j in range(self.Y):
                current_node = self.coordinates_to_vertex_index(row=i, col=j)

                # Connect with the right neighbor (if exists)
                if j + 1 < self.Y:
                    right_neighbor = self.coordinates_to_vertex_index(row=i, col=j + 1)
                    self.adjacency_matrix[current_node, right_neighbor] = 1
                    self.adjacency_matrix[right_neighbor, current_node] = 1

                # Connect with the bottom neighbor (if exists)
                if i + 1 < self.X:
                    bottom_neighbor = self.coordinates_to_vertex_index(row=i + 1, col=j)
                    self.adjacency_matrix[current_node, bottom_neighbor] = 1
                    self.adjacency_matrix[bottom_neighbor, current_node] = 1

        self.apply_special_edges()

    def apply_special_edges(self):
        for special_edge in self.special_edges:
            if special_edge["type"] == "always blocked":
                first_node = self.coordinates_to_vertex_index(row=special_edge["from"][0], col=special_edge["from"][1])
                second_node = self.coordinates_to_vertex_index(row=special_edge["to"][0], col=special_edge["to"][1])

                self.adjacency_matrix[first_node, second_node] = 0
                self.adjacency_matrix[second_node, first_node] = 0

    def is_path_available(self, current_vertex, next_vertex, mode="Coords"):
        # The input vertices are list of coordinates
        if mode == "Coords":
            current_vertex_index = self.coordinates_to_vertex_index(row=current_vertex[0], col=current_vertex[1])
            next_vertex_index = self.coordinates_to_vertex_index(row=next_vertex[0], col=next_vertex[1])
        # The input vertices are indices of the vertices on the graph
        elif mode == "Indices":
            current_vertex_index = current_vertex
            next_vertex_index = next_vertex
        else:
            raise ValueError("Invalid mode")

        # Check if next vertex is occupied
        for agent in self.agents:
            agent_location = agent.get("location", None)
            if agent_location is not None:
                agent_vertex_index = self.coordinates_to_vertex_index(row=agent_location[0], col=agent_location[1])
                if agent_vertex_index == next_vertex_index:
                    return False

        # Check if there is an available edge
        edge_validation = (
            self.adjacency_matrix[current_vertex_index, next_vertex_index] == 0 or
            self.adjacency_matrix[current_vertex_index, next_vertex_index] == 0
        )
        if edge_validation:
            return False

        return True

    def update_state(self, state):
        self.packages = state["packages"]
        self.special_edges = state["special_edges"]
        self.agents = state["agents"]
