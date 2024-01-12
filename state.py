import numpy as np


class State:
    def __init__(self, state_data: dict):
        # Parse state initial parameters
        self.X = state_data["x"] + 1
        self.Y = state_data["y"] + 1
        self.packages = state_data.get("packages", list())
        self.special_edges = state_data.get("special_edges", list())
        self.agents = state_data.get("agents", list())

        # Build state graph
        self.total_vertices = self.X * self.Y
        self.adjacency_matrix = None
        self._build_adjacency_matrix()

        # Parse state additional parameters
        self.time = state_data.get("time", 0)
        self.placed_packages = state_data.get("placed_packages", list())
        self.picked_packages = state_data.get("picked_packages", list())
        self.archived_packages = state_data.get("archived_packages", list())
        self._update_packages_info()

    def coordinates_to_vertex_index(self, row, col):
        if row < 0 or row >= self.X or col < 0 or col >= self.Y:
            raise ValueError("Adjacency Matrix out of bounds")
        return row * self.Y + col

    def _apply_special_edges(self):
        for special_edge in self.special_edges:
            if special_edge["type"] == "always blocked":
                first_node = self.coordinates_to_vertex_index(row=special_edge["from"][0], col=special_edge["from"][1])
                second_node = self.coordinates_to_vertex_index(row=special_edge["to"][0], col=special_edge["to"][1])

                self.adjacency_matrix[first_node, second_node] = 0
                self.adjacency_matrix[second_node, first_node] = 0

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

        self._apply_special_edges()

    def _update_packages_info(self):
        current_packages = self.packages
        for package in current_packages:
            if package["from_time"] <= self.time:
                self.packages.remove(package)
                package["status"] = "placed"
                self.placed_packages.append(package)

        current_placed_packages = self.placed_packages
        for package in current_placed_packages:
            if package["before_time"] <= self.time:
                self.placed_packages.remove(package)
                package["status"] = "disappeared"
                self.archived_packages.append(package)

        current_picked_packages = self.picked_packages
        for package in current_picked_packages:
            if package["before_time"] <= self.time:
                self.picked_packages.remove(package)
                package["status"] = "disappeared"
                package["holder_agent_id"] = -1
                self.archived_packages.append(package)

                for agent_idx, agent in enumerate(self.agents):
                    for agent_package in agent.get("packages", list()):
                        if package["package_id"] == agent_package["package_id"]:
                            self.agents[agent_idx]["packages"].remove(agent_package)

    def is_path_available(self, current_vertex, next_vertex, mode="Coords"):
        # The input vertices are list of coordinates
        if mode == "Coords":
            current_vertex_index = self.coordinates_to_vertex_index(row=current_vertex[0], col=current_vertex[1])
            next_vertex_index = self.coordinates_to_vertex_index(row=next_vertex[0], col=next_vertex[1])
        # The input vertices are indices of the vertices on the graph
        elif mode == "Indices":
            current_vertex_index = current_vertex
            next_vertex_index = next_vertex
        # Encountered invalid mode
        else:
            raise ValueError("Invalid mode")

        # Check if next vertex is occupied
        for agent in self.agents:
            agent_location = agent.get("location", None)
            if agent_location is not None:
                agent_vertex_index = self.coordinates_to_vertex_index(row=agent_location[0], col=agent_location[1])
                if agent_vertex_index == next_vertex_index:
                    return False

        # Check if the edge is missing
        edge_missing_validation = (
            self.adjacency_matrix[current_vertex_index, next_vertex_index] == 0 or
            self.adjacency_matrix[current_vertex_index, next_vertex_index] == 0
        )
        if edge_missing_validation:
            return False

        # All validation passed
        return True

    def print_state(self):
        # Coordinates
        print_data = (
            f"#X {self.X - 1} ; Maximum x coordinate\n"
            f"#Y {self.Y - 1} ; Maximum y coordinate\n"
        )

        # Packages
        all_packages = self.packages + self.placed_packages + self.picked_packages + self.archived_packages
        all_packages.sort(key=lambda p: p["package_id"])
        for package_idx, package in enumerate(all_packages):
            if package["status"] == "waiting":
                p_time = package['from_time']
                print_data += f"#P 0  T {p_time} ; Package {package_idx} is waiting to appear at Time {p_time}\n"
            elif package["status"] == "placed":
                p_x = package["package_at"][0]
                p_y = package["package_at"][1]
                print_data += f"#P 1  L {p_x} {p_y} ; Package {package_idx} was placed on Location ({p_x},{p_y})\n"
            elif package["status"] == "picked":
                p_agent_id = package["holder_agent_id"]
                print_data += f"#P 2  A {p_agent_id} ; Package {package_idx} was picked by Agent {p_agent_id}\n"
            elif package["status"] == "delivered":
                p_agent_id = package["holder_agent_id"]
                print_data += f"#P 3  A {p_agent_id} ; Package {package_idx} was delivered by Agent {p_agent_id}\n"
            elif package["status"] == "disappeared":
                p_time = package["before_time"]
                print_data += f"#P 4  T {p_time} ; Package {package_idx} was disappeared at time {p_time}\n"
            else:
                raise ValueError("Invalid package status")

        print_data += "\n"
        for edge_idx, edge in enumerate(self.special_edges):
            if edge["type"] == "always blocked":
                print_data += f"#E 0 ; Edge {edge_idx} is always blocked\n"
            elif edge["type"] == "fragile":
                print_data += f"#E 1 ; Edge {edge_idx} is fragile\n"
            else:
                raise ValueError("Invalid edge type")

        for agent_idx, agent in enumerate(self.agents):
            if agent["type"] == "Human":
                print_data += f"#A 0 ; Agent {agent_idx} is a Human Agent\n"
            elif agent["type"] == "Normal":
                a_score = agent["score"]
                a_actions = agent["number_of_actions"]
                print_data += (
                    f"#A 1  A {a_actions}  S {a_score} ; "
                    f"Agent {agent_idx} is a Stupid Greedy Agent, Number of Actions: {a_actions}, Score: {a_score}\n"
                )
            elif agent["type"] == "Interfering":
                a_actions = agent["number_of_actions"]
                print_data += (
                    f"#A 2  A {a_actions} ; "
                    f"Agent {agent_idx} is a Saboteur Agent, Number of Actions: {a_actions}\n"
                )
            else:
                raise ValueError("Invalid agent type")

        print(print_data)

    def clone_state(self):
        state_data = {
            "x": self.X - 1,
            "y": self.Y - 1,
            "packages": self.packages,
            "special_edges": self.special_edges,
            "agents": self.agents,
            "time": self.time,
            "placed_packages": self.placed_packages,
            "picked_packages": self.picked_packages
        }
        return State(state_data=state_data)
