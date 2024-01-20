import numpy as np
from state import State


class SearchAlgorithms:
    def __init__(self, state: State):
        self.state = state

    def dijkstra(self, src, dest, mode):
        # convert to node indices
        src_node_index, dest_node_index = self.state.convert_to_node_indices(
            current_vertex=src,
            next_vertex=dest,
            mode=mode
        )

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
            for neighbor_node in range(total_vertices):
                path_validation = (
                    not visited[neighbor_node] and
                    self.state.is_path_available(
                        current_vertex=current_node,
                        next_vertex=neighbor_node,
                        mode="Indices"
                    )
                )
                if path_validation:
                    edge_cost = self.state.edge_cost(
                        current_vertex=current_node,
                        next_vertex=neighbor_node,
                        mode="Indices"
                    )
                    new_distance = distances[current_node] + edge_cost
                    neighbor_distance = float(distances[neighbor_node])
                    distances[neighbor_node] = min(neighbor_distance, new_distance)

        # Check if no path exists from src to dest
        if distances[dest_node_index] == np.inf:
            return np.inf, None, distances

        # Reconstruct the shortest path
        path = [dest_node_index]
        while path[-1] != src_node_index:
            current_node = path[-1]
            previous_nodes = np.where(self.state.adjacency_matrix[:, current_node] > 0)[0]
            previous_node = min(previous_nodes, key=lambda node: distances[node])
            path.append(previous_node)

        # Reverse the path to get it from src to dest
        solution_path = path[::-1]
        # print(f"Solution in vertices indices: {distances[dest_node_index], solution_path}")
        # print(f"Solution in coordinate: {[self.state.vertex_index_to_coordinates(i) for i in solution_path]}")

        return distances[dest_node_index], solution_path, distances

    def dijkstra_step(self, src, dest, mode):
        solution_cost, solution_path, distances = self.dijkstra(src=src, dest=dest, mode=mode)

        if solution_path is not None:
            next_vertex_index = solution_path[1]
            traverse_pos = self.state.vertex_index_to_coordinates(idx=next_vertex_index)
            step_cost = distances[next_vertex_index]
            return solution_cost, traverse_pos, step_cost
        else:
            return None


def test_dijkstra():
    environment_data = {
        "x": 2,
        "y": 2,
        "special_edges": [
            {"type": "always blocked", "from": [0, 0], "to": [0, 1]},
            {"type": "always blocked", "from": [1, 0], "to": [1, 1]},
            # {"type": "always blocked", "from": [2, 1], "to": [2, 2]},
            # {"type": "always blocked", "from": [1, 1], "to": [1, 2]},
            # {"type": "always blocked", "from": [0, 0], "to": [1, 0]}
        ]
    }
    state = State(environment_data=environment_data)
    # print(graph.adjacency_matrix)
    search_algorithms = SearchAlgorithms(state=state)
    sol = search_algorithms.dijkstra_step(src=[0, 0], dest=[2, 2], mode="Coords")
    print(f"Step Solution: {sol}")


if __name__ == "__main__":
    test_dijkstra()
