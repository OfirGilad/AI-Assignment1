from state import State
from search_algorithms import SearchAlgorithms
from informed_search_algorithms import InformedSearchAlgorithms
from node import Node


class TraverseAction:
    def __init__(self, solution_cost, traverse_pos, step_cost):
        self.solution_cost = solution_cost
        self.traverse_pos = traverse_pos
        self.step_cost = step_cost

    # Here and elsewhere, if needed, break ties by preferring lower-numbered vertices in the x Axis
    # and then in the y Axis.
    def __lt__(self, other):
        validation = (
            self.solution_cost < other.solution_cost or
            self.step_cost < other.step_cost or
            (self.solution_cost == other.solution_cost and
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
        return (
            self.solution_cost, self.traverse_pos, self.step_cost
        ) == (
            other.solution_cost, other.traverse_pos, other.step_cost
        )


class Agent:
    def __init__(self, state: State):
        self.state = state
        self.agent_idx = state.agent_idx
        self.agent_action = {
            "Human": self.human_action,
            "Normal": self.stupid_greedy_action,
            "Interfering": self.saboteur_action,
            "Greedy": self.greedy_search_action,
            "A Star": self.a_star_action,
            "Real time A Star": self.real_time_a_star_action
        }

    def human_action(self):
        while True:
            user_input = input("(Human) Enter your action: ")
            if user_input == "print":
                print(self.state.print_state())
            elif user_input == "next":
                break
            else:
                print(f"Invalid input: {user_input}! Write either 'print' or 'next'.")

        return self.state, "no-op"

    def stupid_greedy_action(self):
        # Update agent picked and delivered packages
        self.state.update_agent_packages_status()

        agent_data = self.state.agents[self.agent_idx]
        search_algorithms = SearchAlgorithms(state=self.state)

        traverse_actions = list()
        # Find path for packages to deliver
        if len(agent_data["packages"]) > 0:
            for package in agent_data["packages"]:
                step = search_algorithms.dijkstra_step(
                    src=agent_data["location"],
                    dest=package["deliver_to"],
                    mode="Coords"
                )
                if step is not None:
                    solution_cost, traverse_pos, step_cost = step
                    traverse_actions.append(TraverseAction(
                        solution_cost=solution_cost,
                        traverse_pos=traverse_pos,
                        step_cost=step_cost
                    ))
        # Find path for packages to collect
        else:
            for package in self.state.placed_packages:
                step = search_algorithms.dijkstra_step(
                    src=agent_data["location"],
                    dest=package["package_at"],
                    mode="Coords"
                )
                if step is not None:
                    solution_cost, traverse_pos, step_cost = step
                    traverse_actions.append(TraverseAction(
                        solution_cost=solution_cost,
                        traverse_pos=traverse_pos,
                        step_cost=step_cost
                    ))

        if len(traverse_actions) == 0:
            return self.state, "no-op"
        else:
            minimum_cost_action = min(traverse_actions)
            next_traverse_pos = minimum_cost_action.traverse_pos
            action_name = self.state.perform_agent_step(
                current_vertex=agent_data["location"],
                next_vertex=next_traverse_pos,
                mode="Coords"
            )
            self.state.update_agent_packages_status()
            return self.state, action_name

    def saboteur_action(self):
        agent_data = self.state.agents[self.agent_idx]
        search_algorithms = SearchAlgorithms(state=self.state)
        traverse_actions = list()
        
        # Find path a to a fragile edge
        for edge in self.state.special_edges:
            if edge["type"] == "fragile" and agent_data["location"] != edge["from"]:
                step = search_algorithms.dijkstra_step(
                    src=agent_data["location"],
                    dest=edge["from"],
                    mode="Coords"
                )
                if step is not None:
                    solution_cost, traverse_pos, step_cost = step
                    traverse_actions.append(TraverseAction(
                        solution_cost=solution_cost,
                        traverse_pos=traverse_pos,
                        step_cost=step_cost
                    ))
            if edge["type"] == "fragile" and agent_data["location"] != edge["to"]:
                step = search_algorithms.dijkstra_step(
                    src=agent_data["location"],
                    dest=edge["to"],
                    mode="Coords"
                )
                if step is not None:
                    solution_cost, traverse_pos, step_cost = step
                    traverse_actions.append(TraverseAction(
                        solution_cost=solution_cost,
                        traverse_pos=traverse_pos,
                        step_cost=step_cost
                    ))    
                    
        if len(traverse_actions) == 0:
            return self.state, "no-op"
        else:
            minimum_cost_action = min(traverse_actions)
            next_traverse_pos = minimum_cost_action.traverse_pos
            action_name = self.state.perform_agent_step(
                current_vertex=agent_data["location"],
                next_vertex=next_traverse_pos,
                mode="Coords"
            )
            return self.state, action_name

    def greedy_search_action(self):
        node = Node(state=self.state)
        node.expand()
        best_node = min(node.get_children(), key=lambda child_node: child_node.h_value())
        best_node.state.time -= 1
        return best_node.state, best_node.get_action()

    def a_star_action(self):
        node = Node(state=self.state)
        a_star = InformedSearchAlgorithms(initial_node=node, is_limited=True)
        a_star_res = a_star.A_star()
        if a_star_res != "fail":
            state, action = a_star_res
            if action != "no-op":
                state.time -= 1
            return state, action
        return self.state, "no-op"

    def real_time_a_star_action(self):
        node = Node(state=self.state)
        a_star = InformedSearchAlgorithms(initial_node=node, is_limited=False, L=10)
        a_star_res = a_star.A_star()
        if a_star_res != "fail":
            state, action = a_star_res
            if action != "no-op":
                state.time -= 1
            return state, action
        return self.state, "no-op"

    def perform_action(self):
        agent_type = self.state.agents[self.agent_idx]["type"]
        state, action = self.agent_action[agent_type]()
        return state, action


def test_agents():
    
    environment_data = {
        "x": 2,
        "y": 2,
        "special_edges": [
            # {"type": "always blocked", "from": [0, 0], "to": [0, 1]},
            # {"type": "always blocked", "from": [1, 0], "to": [1, 1]},
            # {"type": "always blocked", "from": [2, 1], "to": [2, 2]},
            # {"type": "always blocked", "from": [1, 1], "to": [1, 2]},
            # {"type": "always blocked", "from": [0, 0], "to": [1, 0]}
        ],
        "agents": [
            {
                # "type": "Greedy",
                "type": "A Star",
                # "type": "Real time A Star",
                "location": [2, 2],
                "score": 0,
                "packages": list(),
                "number_of_actions": 0
            }
        ],
        "placed_packages": [
            {
                "package_at": [2, 1],
                "from_time": 0,
                "deliver_to": [2, 0],
                "before_time": 10,
                "package_id": 0,
                "status": "placed",
                "holder_agent_id": -1
            },
            {
                "package_at": [0, 2],
                "from_time": 0,
                "deliver_to": [1, 0],
                "before_time": 10,
                "package_id": 0,
                "status": "placed",
                "holder_agent_id": -1
            }
        ],
        "agent_idx": 0
    }
    state = State(environment_data=environment_data)
    # print(graph.adjacency_matrix)
    # node = Node(state=state)
    # print(node.search_adjacency_matrix)
    # print(node.search_adjacency_matrix_mst)
    # print(node.heuristic_value)    
    a = Agent(state)
    state, action = a.perform_action()
    print(state.print_state(), action)


if __name__ == "__main__":
    test_agents()
