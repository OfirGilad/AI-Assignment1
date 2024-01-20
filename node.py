from state import State


class Node:
    def __init__(self, state: State, parent=None, action="no-op"):
        self.state = state
        self.agent_idx = state.agent_idx
        self.parent = parent
        self.children = list()

        self.action = action
        self.depth = 0
        self.path_cost = 0
        self.heuristic_value = 0
        self._read_parent_data()

    def _calculate_action_cost(self):
        parent_location = self.parent.state.agents[self.agent_idx]["location"]
        node_location = self.state.agents[self.agent_idx]["location"]
        action_cost = self.state.edge_cost(parent_location, node_location)
        return action_cost

    def _read_parent_data(self):
        if self.parent is not None:
            self.depth += self.parent.depth
            self.path_cost += self.parent.path_cost + self._calculate_action_cost()

    def expand(self):
        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        node_location = self.state.agents[self.agent_idx]["location"]
        for move in possible_moves:
            new_location = [node_location[0] + move[0], node_location[1] + move[1]]
            if self.state.is_path_available(current_vertex=node_location, next_vertex=new_location, mode="Coords"):
                # Create new node with time passed by 1
                node_state = self.state.clone_state(agent_idx=self.agent_idx, time_factor=1)
                action = node_state.perform_agent_step(
                    current_vertex=node_location,
                    next_vertex=new_location,
                    mode="Coords"
                )
                self.state.update_agent_packages_status()

                child = Node(
                    state=self.state,
                    parent=self,
                    action=action
                )
                self.children.append(child)

    def h_value(self):
        return self.heuristic_value

    def g_value(self):
        return self.path_cost

    def f_value(self):
        return self.g_value() + self.h_value()
