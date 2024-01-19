from ascii_parser import Parser
from state import State
from simulator import Simulator


def main():
    data_file_path = "./input.txt"
    parser = Parser()
    environment_data = parser.parse_data(data_filepath=data_file_path)
    # print(parse_data)
    initial_state = State(environment_data=environment_data)
    # print(initial_state.adjacency_matrix)
    simulator = Simulator(initial_state=initial_state)
    simulator.run()


if __name__ == '__main__':
    main()
