import re
import logging

LOG = logging.getLogger()
LOG.setLevel("INFO")


def get_input(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


class SquareArray:
    def __init__(self, in_array):
        assert len(in_array) == len(in_array[0])
        self.in_array = in_array
        self.size = len(in_array)

    def get_col(self, i):
        return "".join([row[i] for row in self.in_array])

    def get_diagonal(self, diag):
        if diag >= 0:
            return "".join([self.in_array[i][i + diag] for i in range(self.size - diag)])
        else:
            return "".join([self.in_array[i - diag][i] for i in range(self.size + diag)])

    def get_reversed_diagonal(self, diag):
        if diag >= 0:
            return "".join([self.in_array[self.size - 1 - i][i + diag] for i in range(self.size - diag)])
        else:
            return "".join([self.in_array[self.size - 1 - i + diag][i] for i in range(self.size + diag)])


def find_xmases(line):
    return len(re.findall("XMAS", line)) + len(re.findall("SAMX", line))


def part1(puzzle_input):
    total_xmases = 0
    square_array = SquareArray(puzzle_input)
    for i, line in enumerate(square_array.in_array):
        horizontal_xmases = find_xmases(line)
        # print(f"{horizontal_xmases=} at row {i=}")
        total_xmases += horizontal_xmases
    for i in range(square_array.size):
        vertical_xmases = find_xmases(square_array.get_col(i))
        # print(f"{vertical_xmases=} at col {i=}")
        total_xmases += vertical_xmases
    for i in range(-square_array.size + 1, square_array.size):
        diagonal_xmases = find_xmases(square_array.get_diagonal(i))
        # print(f"{diagonal_xmases=} at diag {i=}")
        total_xmases += diagonal_xmases
    for i in range(-square_array.size + 1, square_array.size):
        reversed_diagonal_xmases = find_xmases(square_array.get_reversed_diagonal(i))
        # print(f"{reversed_diagonal_xmases=} at diag {i=}")
        total_xmases += reversed_diagonal_xmases
    return total_xmases


def part2(puzzle_input):
    allowed_configs = {
        ("M", "M", "S", "S"),
        # ("M", "S", "M", "S"),  # Corresponds to "MAM" and "SAS"!
        ("M", "S", "S", "M"),
        ("S", "M", "M", "S"),
        # ("S", "M", "S", "M"),  # Corresponds to "MAM" and "SAS"!
        ("S", "S", "M", "M")
    }
    total_xmases = 0
    for i in range(1, len(puzzle_input) - 1):
        for j in range(1, len(puzzle_input) - 1):
            if puzzle_input[i][j] == "A":
                if (puzzle_input[i - 1][j - 1], puzzle_input[i - 1][j + 1], puzzle_input[i + 1][j + 1], puzzle_input[i + 1][j - 1]) in allowed_configs:
                    # print(f"It' a match at {i=}, {j=}")
                    total_xmases += 1
    return total_xmases


def main():
    puzzle_input = get_input("test_files/prob4_full_input.txt")
    print(f"Solution to part 1 is: {part1(puzzle_input)}")
    print(f"Solution to part 2 is: {part2(puzzle_input)}")


if __name__ == "__main__":
    main()
