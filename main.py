def handle_x(line_data_args):
    return True


def handle_y(line_data_args):
    return True


def handle_p(line_data_args):
    return True


def handle_b(line_data_args):
    return True


def handle_f(line_data_args):
    return True


def handle_a(line_data_args):
    return True


def handle_h(line_data_args):
    return True


def handle_i(line_data_args):
    return True


def parse_data(data_filepath):
    options_dict = {
        "#X": handle_x,
        "#Y": handle_y,
        "#P": handle_p,
        "#B": handle_b,
        "#F": handle_f,
        "#A": handle_a,
        "#H": handle_h,
        "#I": handle_i
    }
    with open(data_filepath) as data_file:
        line_data = data_file.readline()
        while line_data != "":
            line_data_args = line_data.split()
            if line_data_args[0] in options_dict.keys():
                option_result = options_dict[line_data_args[0]](line_data_args)
            line_data = data_file.readline()


def main():
    data_file_path = "./input.txt"
    parse_data(data_filepath=data_file_path)


if __name__ == '__main__':
    parsed_data = dict()
    main()
