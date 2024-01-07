from parser import Parser
from graph import Graph


def main():
    data_file_path = "./input.txt"
    parse_data = Parser().parse_data(data_filepath=data_file_path)
    print(parse_data)
    graph = Graph(parsed_data=parse_data)
    print(graph.adjacency_matrix)


if __name__ == '__main__':
    main()
