from graph import Graph


class SearchAlgorithms:
    def __init__(self, graph: Graph):
        self.graph = graph

    # Returns the shortest path to (targetX,targetY) and the second vertex in the shortest path
    def solution(self, dist, prev, srcX, srcY, targetX, targetY):
        S = []
        u = [targetX, targetY]
        # Verify vertex is reachable
        if prev[targetX, targetY] is None:
            return 1e7, []
        if prev[u[0], u[1]] is not None or (u[0], u[1]) == (srcX, srcY):
            while u is not None:
                S.append(u)
                u = prev[u[0], u[1]]
        return dist[targetX, targetY], S[-2]

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in the shortest path tree
    def min_distance(self, dist, sptSet):
        # Initialize minimum distance for next node
        min = 1e7
        min_index = None

        # Search not nearest vertex not in the
        # shortest path tree
        for vX in range(0, self.graph.X, 1):
            for vY in range(0, self.graph.Y, 1):
                if dist[vX, vY] < min and sptSet[vX, vY] is False:
                    min = dist[vX, vY]
                    min_index = vX, vY

        return min_index

    # Function that implements Dijkstra's single source
    # the shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, srcX, srcY, targetX, targetY):
        dist = ([0] * self.graph.Y) * self.graph.X
        dist[srcX, srcY] = 0
        prev = ([None] * self.graph.Y) * self.graph.X
        sptSet = ([False] * self.graph.Y) * self.graph.X

        for cX in range(0, self.graph.X, 1):
            for cY in range(0, self.graph.Y, 1):
                # Pick the minimum distance vertex from
                # the set of vertices not yet processed.
                # u is always equal to src in first iteration
                uX, uY = self.min_distance(dist, sptSet)
                if (targetX, targetY) == (uX, uY):
                    return

                # Put the minimum distance vertex in the
                # shortest path tree
                sptSet[uX, uY] = True

                # Update dist value of the adjacent vertices
                # of the picked vertex only if the current
                # distance is greater than new distance and
                # the vertex in not in the shortest path tree
                for vX in range(0, self.X, 1):
                    for vY in range(0, self.Y, 1):
                        for edge in self.graph.special_edges:
                            for agent in self.graph.agents:
                                if edge["type"] != "always blocked" and agent["location"] != [vX, vY] and edge["from"] == [uX, uY] and edge["to"] == [vX, vY] and sptSet[vX, vY] is False and dist[vX, vY] > dist[uX, uY] + 1:
                                    dist[vX, vY] = dist[uX, uY] + 1
                                    prev[vX, vY] = [uX, uY]

        return self.solution(dist, prev, srcX, srcY, targetX, targetY)
