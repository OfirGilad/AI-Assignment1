from agents import Agent
from state import State


class Simulator:
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.states = [self.current_state]

        # self.state = {
        #     "x": parsed_data["x"],
        #     "y": parsed_data["y"],
        #     "pool_packages": parsed_data["packages"],
        #     # Packages which appeared and are not picked up
        #     "placed_packages": list(),
        #     # Packages that are picked up
        #     "pickedUp_packages": list(),
        #     "edges": parsed_data["edges"],
        #     "agents": parsed_data["agents"],
        #     "time": 0
        # }
        # self.options_dict = {
        #     "#X": self._handle_x,
        #     "#Y": self._handle_y,
        #     "#P": self._handle_p,
        #     "#B": self._handle_b,
        #     "#F": self._handle_f,
        #     "#A": self._handle_a,
        #     "#H": self._handle_h,
        #     "#I": self._handle_i
        # }

    # # A stupid greedy agent
    # def _handle_a(self, agent):
    #     # A robot agent (pickup and delivery robot) at a vertex automatically picks up a package at that vertex
    #     # if there is one.
    #     for package in self.state["placed_packages"]:
    #         if package["package_at"] == agent["location"] and package["from_time"] <= package["time"]:
    #             agent["packages"].append(package)
    #             self.state["placed_packages"].remove(package)
    #             self.state["pickedUp_packages"].append(package)
    #
    #     for package in agent["packages"]:
    #         # The robot agent delivers the packages and scores
    #         if package["deliver_to"] == agent["location"] and package["before_time"]>package["time"]:
    #             agent["packages"].remove(package)
    #             agent["score"] += 1
    #             self.state["pickedUp_packages"].remove(package)
    #         # The deadline to deliver this packages has passed
    #         if package["before_time"] <= self.state["time"]:
    #             agent["packages"].remove(package)
    #             self.state["pickedUp_packages"].remove(package)
    #
    #     graph = Graph(self.state)
    #     search_algorithms = SearchAlgorithms(graph=graph)
    #     # If the agent is not holding a package, it should compute the shortest currently unblocked path to
    #     # the next vertex with a package to be delivered, and try to follow it.
    #     if len(agent["packages"]) == 0:
    #         paths = []
    #         for package in self.state["placed_packages"]:
    #             cost, traversePos = search_algorithms.dijkstra(
    #                 agent["location"][0],
    #                 agent["location"][1],
    #                 package["package_at"][0],
    #                 package["package_at"][1]
    #             )
    #             if (cost, traversePos) != (1e7, []):
    #                 paths.append(TraverseAction(cost, traversePos))
    #
    #         if len(paths) == 0:
    #             return "no-op"
    #
    #         else:
    #             _, nextTraversePos = min(paths)
    #
    #             for edge in self.state["edges"]:
    #                 if edge["from"] == agent["location"] and edge["to"] == nextTraversePos and edge["type"] == "fragile":
    #                     edge["type"] = "always blocked"
    #
    #             agent["location"] = nextTraversePos
    #
    #     # If it is holding a package, it should find the shortest path to a delivery location for the package,
    #     # and try to follow it.
    #     # If holding more than 1 package, attempt to deliver the one with a shorter path to its delivery location.
    #     else:
    #         paths = []
    #         for package in agent["packages"]:
    #             cost, traversePos = search_algorithms.dijkstra(
    #                 agent["location"][0],
    #                 agent["location"][1],
    #                 package["deliver_to"][0],
    #                 package["deliver_to"][1]
    #             )
    #             if (cost, traversePos) != (1e7, []):
    #                 paths.append(TraverseAction(cost, traversePos))
    #
    #         if len(paths) == 0:
    #             return "no-op"
    #
    #         else:
    #             #### Verify cost matches the deadline???
    #             cost, nextTraversePos = min(paths)
    #             for edge in self.state["edges"]:
    #                 if edge["from"] == agent["location"] and edge["to"] == nextTraversePos and edge["type"] == "fragile":
    #                     edge["type"] = "always blocked"
    #             agent["location"] = nextTraversePos

    # Extract packages from their pool and place them if it is their time to appear.
    # Remove any unpicked package whose time to be delivered has passed
    # def distribute_packages(self):
    #     for package in self.state["pool_packages"]:
    #         if package["from_time"] <= self.state["time"]:
    #             self.state["pool_packages"].remove(package)
    #             self.state["placed_packages"].append(package)
    #
    #     for package in self.state["placed_packages"]:
    #         if package["before_time"] <= self.state["time"]:
    #             self.state["placed_packages"].remove(package)

    # def simulate(self):
    #     self.distribute_packages()
    #     # The simulation ends when all packages have been delivered, or there is no path for any agent to pick up
    #     # or deliver any more packages on time.
    #     if len(self.state["pool_packages"]) == 0 and len(self.state["placed_packages"]) == 0 and len(self.state["pickedUp_packages"]) == 0:
    #         return
    #
    #     #### Simulation content
    #     self.state["time"] += 1

    def _goal_achieved(self):
        goal_validation = (
            len(self.current_state.packages) == 0 and
            len(self.current_state.placed_packages) == 0 and
            len(self.current_state.picked_packages) == 0
        )
        if goal_validation:
            return True
        else:
            return False

    def run(self):
        agent_idx = 0
        print("Cycle 0:")
        while True:
            # Check if goal achieved
            if self._goal_achieved():
                break

            # Perform Agent Action
            print(f"Agent {agent_idx} ({self.current_state.agents[agent_idx]['type']}) Turn")
            self.current_state = self.current_state.clone_state()
            current_agent = Agent(agent_idx=agent_idx, state=self.current_state)
            self.current_state = current_agent.perform_action()
            self.states.append(self.current_state)

            # Update end of turn parameters
            agent_idx = (agent_idx + 1) % len(self.current_state.agents)
            if agent_idx == 0:
                self.current_state.time += 1
                print(f"Cycle {self.current_state.time}")
