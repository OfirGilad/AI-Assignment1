import numpy as np

from state import State
from search_algorithms import SearchAlgorithms


class TraverseAction:
    def __init__(self, cost, traverse_pos):
        self.cost = cost
        self.traverse_pos = traverse_pos

    # Here and elsewhere, if needed, break ties by preferring lower-numbered vertices in the x axis
    # and then in the y axis.
    def __lt__(self, other):
        validation = (
            self.cost < other.cost or
            (self.cost == other.cost and
                (self.traverse_pos[0] < other.traverse_pos[0] or
                    (self.traverse_pos[0] == other.traverse_pos[0] and
                        self.traverse_pos[1] < other.traverse_pos[1]
                     )
                 )
             )
        )
        return validation

    # Two objects are defined as identical if their state are equal
    def __eq__(self, other):
        return (self.cost, self.traverse_pos) == (other.cost, other.traversePos)


class Agent:
    def __init__(self, agent_idx: int, state: State):
        self.agent_idx = agent_idx
        self.state = state
        self.agent_action = {
            "Human": self.human_action,
            "Normal": self.stupid_greedy_action,
            "Interfering": self.saboteur_action
        }

    def human_action(self):
        while True:
            user_input = input("(Human) Enter your action: ")
            if user_input == "print":
                self.state.print_state()
            elif user_input == "next":
                break
            else:
                print("Invalid input! Write either 'print' or 'next'.")

    def _update_packages_status(self, agent_data):
        current_placed_packages = self.state.placed_packages
        for package in current_placed_packages:
            if package["package_at"] == agent_data["location"]:
                agent_data["packages"].append(package)
                self.state.placed_packages.remove(package)
                package["status"] = "picked"
                package["holder_agent_id"] = self.agent_idx
                self.state.picked_packages.append(package)

        current_pickup_packages = self.state.picked_packages
        for package in current_pickup_packages:
            if package["deliver_to"] == agent_data["location"]:
                agent_data["packages"].remove(package)
                self.state.picked_packages.remove(package)
                package["status"] = "delivered"
                self.state.archived_packages.append(package)

                agent_data["packages"].remove(package)
                agent_data["score"] += 1

        return agent_data

    def stupid_greedy_action(self):
        agent_data = self.state.agents[self.agent_idx]

        # A robot agent (pickup and delivery robot) at a vertex automatically picks up a package at that vertex
        # if there is one.
        agent_data = self._update_packages_status(agent_data=agent_data)

        search_algorithms = SearchAlgorithms(state=self.state)
        # If the agent is not holding a package, it should compute the shortest currently unblocked path to
        # the next vertex with a package to be delivered, and try to follow it.
        if len(agent_data["packages"]) == 0:
            paths = []
            for package in self.state.placed_packages:
                cost, traverse_pos = search_algorithms.dijkstra(src=agent_data["location"], dest=package["package_at"])
                if (cost, traverse_pos) != (np.inf, []):
                    paths.append(TraverseAction(cost, traverse_pos))

            if len(paths) == 0:
                return "no-op"

            else:
                _, nextTraversePos = min(paths)

                for edge in self.state.special_edges:
                    if edge["from"] == agent_data["location"] and edge["to"] == nextTraversePos and edge["type"] == "fragile":
                        edge["type"] = "always blocked"

                agent_data["location"] = nextTraversePos

        # If it is holding a package, it should find the shortest path to a delivery location for the package,
        # and try to follow it.
        # If holding more than 1 package, attempt to deliver the one with a shorter path to its delivery location.
        else:
            paths = []
            for package in agent_data["packages"]:
                cost, traverse_pos = search_algorithms.dijkstra(
                    src=agent_data["location"],
                    dest=package["deliver_to"]
                )
                if (cost, traverse_pos) != (np.inf, []):
                    paths.append(TraverseAction(cost, traverse_pos))

            if len(paths) == 0:
                return "no-op"

            else:
                #### Verify cost matches the deadline???
                cost, nextTraversePos = min(paths)
                for edge in self.state.special_edges:
                    if edge["from"] == agent_data["location"] and edge["to"] == nextTraversePos and edge["type"] == "fragile":
                        edge["type"] = "always blocked"
                agent_data["location"] = nextTraversePos

    def saboteur_action(self):
        return True

    def perform_action(self):
        agent_type = self.state.agents[self.agent_idx]["type"]
        self.agent_action[agent_type]()
        return self.state
