from agents import Agent
from state import State


class Simulator:
    def __init__(self, initial_state: State):
        self.no_op_count = 0
        self.normal_agents_count = len([agent for agent in initial_state.agents if agent["type"] == "Normal"])
        self.current_state = initial_state
        self.states = [self.current_state]

    def _goal_achieved(self):
        goal1_validation = (
            len(self.current_state.packages) == 0 and
            len(self.current_state.placed_packages) == 0 and
            len(self.current_state.picked_packages) == 0
        )
        goal2_validation = (
            len(self.current_state.packages) == 0 and
            self.no_op_count == self.normal_agents_count
        )
        if goal1_validation:
            print("Goal achieved: All available packages have been delivered")
            return True
        elif goal2_validation:
            print("Goal achieved: There is no path for any agent to pick up or deliver any more packages on time")
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
            self.current_state = self.current_state.clone_state()
            current_agent = Agent(agent_idx=agent_idx, state=self.current_state)
            self.current_state, action = current_agent.perform_action()
            self.states.append(self.current_state)

            # Print Agent Action
            agent_type = self.current_state.agents[agent_idx]['type']
            print(f"Agent {agent_idx} ({agent_type}) Action: {action}")
            if action == "no-op" and agent_type == "Normal":
                self.no_op_count += 1

            # Update end of turn parameters
            agent_idx = (agent_idx + 1) % len(self.current_state.agents)
            if agent_idx == 0:
                self.no_op_count = 0
                self.current_state.time += 1
                print(f"Cycle {self.current_state.time}")
