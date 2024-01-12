import numpy as np
from state import State


class SearchAlgorithms:
    def __init__(self, state: State):
        self.state = state

    def dijkstra(self, src: list, dest: list):
        # convert coordinates to node indices
        src_node_index = self.state.coordinates_to_vertex_index(row=src[0], col=src[1])
        dest_node_index = self.state.coordinates_to_vertex_index(row=dest[0], col=dest[1])

        # Initialize distance array with infinity for all nodes except the source node
        total_vertices = self.state.total_vertices
        distances = np.full(total_vertices, np.inf)
        distances[src_node_index] = 0

        # Initialize an array to keep track of visited nodes
        visited = np.zeros(total_vertices, dtype=bool)

        # Main Dijkstra's algorithm loop
        for _ in range(total_vertices):
            # Find the unvisited node with the smallest distance
            min_dist = np.inf
            current_node = None

            for vertex_index in range(self.state.total_vertices):
                if distances[vertex_index] < min_dist and not visited[vertex_index]:
                    min_dist = distances[vertex_index]
                    current_node = vertex_index

            # Stop the algorithm if the destination is unreachable
            if current_node is None:
                break

            # Mark the current node as visited
            visited[current_node] = True

            # Stop the algorithm if the destination is reached
            if current_node == dest_node_index:
                break

            # Update the distance array based on the current node
            for neighbor in range(total_vertices):
                path_validation = (
                    not visited[neighbor] and
                    self.state.is_path_available(current_vertex=current_node, next_vertex=neighbor, mode="Indices")
                )
                if path_validation:
                    new_distance = distances[current_node] + self.state.adjacency_matrix[current_node, neighbor]
                    neighbor_distance = float(distances[neighbor])
                    distances[neighbor] = min(neighbor_distance, new_distance)

        # Reconstruct the shortest path
        path = list()
        if distances[dest_node_index] == np.inf:
            # No path exists from src to dest
            return np.inf, path

        path.append(dest_node_index)
        while path[-1] != src_node_index:
            current_node = path[-1]
            previous_nodes = np.where(self.state.adjacency_matrix[:, current_node] > 0)[0]
            previous_node = min(previous_nodes, key=lambda node: distances[node])
            path.append(previous_node)

        # Reverse the path to get it from src to dest
        return distances[dest_node_index], path[::-1]


def test_dijkstra():
    parsed_data = {
        "x": 2,
        "y": 2,
        "special_edges": [
            {"type": "always blocked", "from": [0, 0], "to": [0, 1]},
            {"type": "always blocked", "from": [1, 0], "to": [1, 1]},
            {"type": "always blocked", "from": [2, 1], "to": [2, 2]},
            {"type": "always blocked", "from": [1, 1], "to": [1, 2]},
            # {"type": "always blocked", "from": [0, 0], "to": [1, 0]}
        ]
    }
    state = State(state_data=parsed_data)
    # print(graph.adjacency_matrix)
    search_algorithms = SearchAlgorithms(state=state)
    sol = search_algorithms.dijkstra(src=[0, 0], dest=[2, 2])
    print(f"Solution: {sol}")


if __name__ == "__main__":
    test_dijkstra()
