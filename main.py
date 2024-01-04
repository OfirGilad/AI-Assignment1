from parser import Parser


def main():
    data_file_path = "./input.txt"
    parse_data = Parser().parse_data(data_filepath=data_file_path)
    print(parse_data)


if __name__ == '__main__':
    main()
