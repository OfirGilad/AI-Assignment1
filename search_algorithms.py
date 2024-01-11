import numpy as np
from graph import Graph


class SearchAlgorithms:
    def __init__(self, graph: Graph):
        self.graph = graph

    # # Returns the shortest path to (dest_x, dest_y) and the second vertex in the shortest path
    # @staticmethod
    # def solution(dist, prev, src_x, src_y, dest_x, dest_y):
    #     sol = list()
    #     u = [dest_x, dest_y]
    #
    #     # Verify vertex is reachable
    #     if prev[dest_x, dest_y] is None:
    #         return 1e7, list()
    #     if prev[u[0], u[1]] is not None or (u[0], u[1]) == (src_x, src_y):
    #         while u is not None:
    #             sol.append(u)
    #             u = prev[u[0], u[1]]
    #     return dist[dest_x, dest_y], sol[-2]
    #
    # # A utility function to find the vertex with minimum distance value, from the set of vertices
    # # not yet included in the shortest path tree
    # def min_distance(self, dist, spt_set):
    #     # Initialize minimum distance for next node
    #     min_dist = 1e7
    #     min_index = None
    #
    #     # Search not nearest vertex not in the shortest path tree
    #     for v_x in range(0, self.graph.X, 1):
    #         for v_y in range(0, self.graph.Y, 1):
    #             if dist[v_x, v_y] < min_dist and spt_set[v_x, v_y] == False:
    #                 min_dist = dist[v_x, v_y]
    #                 min_index = v_x, v_y
    #
    #     return min_index
    #
    # # Function that implements Dijkstra's single source the shortest path algorithm for a graph represented
    # # using adjacency matrix representation
    # def dijkstra(self, src, dest):
    #     src_x, src_y = src
    #     dest_x, dest_y = dest
    #     total_vertices = self.graph.X * self.graph.Y
    #     dist = np.zeros(shape=(total_vertices, total_vertices), dtype=np.float32)
    #     dist[src_x, src_y] = 0
    #     prev = ([None] * self.graph.Y) * self.graph.X
    #     spt_set = np.zeros(shape=(total_vertices, total_vertices), dtype=bool)
    #
    #     for c_x in range(0, self.graph.X, 1):
    #         for c_y in range(0, self.graph.Y, 1):
    #             # Pick the minimum distance vertex from the set of vertices not yet processed.
    #             # u is always equal to src in first iteration
    #             u_x, u_y = self.min_distance(dist=dist, spt_set=spt_set)
    #             if (dest_x, dest_y) == (u_x, u_y):
    #                 return
    #
    #             # Put the minimum distance vertex in the shortest path tree
    #             spt_set[u_x, u_y] = True
    #
    #             # Update dist value of the adjacent vertices of the picked vertex only if the current
    #             # distance is greater than new distance and the vertex in not in the shortest path tree
    #             for v_x in range(0, self.graph.X, 1):
    #                 for v_y in range(0, self.graph.Y, 1):
    #                     validation = (
    #                         self.graph.is_path_available(current_vertex=[u_x, u_y], next_vertex=[v_x, v_y]) and
    #                         spt_set[v_x, v_y] == False
    #                         # dist[v_x, v_y] > dist[u_x, u_y] + 1
    #                     )
    #                     if validation:
    #                         dist[v_x, v_y] = dist[u_x, u_y] + 1
    #                         prev[v_x, v_y] = [u_x, u_y]
    #
    #     return self.solution(dist=dist, prev=prev, src_x=src_x, src_y=src_y, dest_x=dest_x, dest_y=dest_y)

    def dijkstra(self, src: list, dest: list):
        # convert coordinates to node indices
        src_node_index = self.graph.coordinates_to_vertex_index(row=src[0], col=src[1])
        dest_node_index = self.graph.coordinates_to_vertex_index(row=dest[0], col=dest[1])

        # Initialize distance array with infinity for all nodes except the source node
        total_vertices = self.graph.total_vertices
        distances = np.full(total_vertices, np.inf)
        distances[src_node_index] = 0

        # Initialize an array to keep track of visited nodes
        visited = np.zeros(total_vertices, dtype=bool)

        # Main Dijkstra's algorithm loop
        for _ in range(total_vertices):
            # Find the unvisited node with the smallest distance
            min_dist = np.inf
            current_node = None

            for vertex_index in range(self.graph.total_vertices):
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
                    self.graph.is_path_available(current_vertex=current_node, next_vertex=neighbor, mode="Indices")
                )
                if path_validation:
                    new_distance = distances[current_node] + self.graph.adjacency_matrix[current_node, neighbor]
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
            previous_nodes = np.where(self.graph.adjacency_matrix[:, current_node] > 0)[0]
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
    graph = Graph(parsed_data=parsed_data)
    # print(graph.adjacency_matrix)
    search_algorithms = SearchAlgorithms(graph=graph)
    sol = search_algorithms.dijkstra(src=[0, 0], dest=[2, 2])
    print(f"Solution: {sol}")


if __name__ == "__main__":
    test_dijkstra()
