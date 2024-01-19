from state import State


class Node:
    def __init__(self, agent_idx: int, state: State, parent=None, action="no-op"):
        self.agent_idx = agent_idx
        self.state = state
        self.parent = parent
        self.children = list()

        self.action = action
        self.depth = 0
        self.path_cost = 0
        self._read_parent_data()

    def _calculate_action_cost(self):
        # TODO: build action cost calculation
        return 1

    def _read_parent_data(self):
        if self.parent is not None:
            self.depth += self.parent.depth
            self.path_cost += self.parent.path_cost + self._calculate_action_cost()

    def expand(self, child):
        # TODO: build loop for building actions
        self.children.append(child)

    def heuristic(self):
        # TODO: build heuristic function
        return 0
