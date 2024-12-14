from collections import defaultdict


def get_input(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


class Vector:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, other):
        return Vector(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        return Vector(self.row - other.row, self.col - other.col)

    def __neg__(self):
        return Vector(-self.row, -self.col)

    def __str__(self):
        return f"Vector({self.row}, {self.col})"

    def __repr__(self):
        return f"Vector({self.row}, {self.col})"

    def is_outside(self, num_rows, num_cols):
        if (0 <= self.row < num_rows) and (0 <= self.col < num_cols):
            return False
        return True

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


def visualise_map(antinodes, puzzle_input):
    for i, line in enumerate(puzzle_input):
        line_to_print = list(line)
        for j in range(len(line)):
            if Vector(i, j) in antinodes:
                line_to_print[j] = "#"
        print("".join(line_to_print))


def get_frequency_dict(puzzle_input):
    frequency_dict = defaultdict(list)
    for i, line in enumerate(puzzle_input):
        for j in range(len(line)):
            if puzzle_input[i][j] != ".":
                frequency_dict[puzzle_input[i][j]].append(Vector(i, j))
    return frequency_dict


def part1(puzzle_input):
    num_rows, num_cols = len(puzzle_input), len(puzzle_input[0])
    frequency_dict = get_frequency_dict(puzzle_input)
    antinode_positions = set()
    for frequency in frequency_dict:
        frequency_positions = frequency_dict[frequency]
        for i, position in enumerate(frequency_positions):
            for j in range(i + 1, len(frequency_positions)):
                antenna_one, antenna_two = frequency_positions[i], frequency_positions[j]
                one_to_two_vector = antenna_two - antenna_one
                antinode_position1 = antenna_one - one_to_two_vector
                if not antinode_position1.is_outside(num_rows, num_cols):
                    antinode_positions.add(antinode_position1)
                antinode_position2 = antenna_two + one_to_two_vector
                if not antinode_position2.is_outside(num_rows, num_cols):
                    antinode_positions.add(antinode_position2)
    # visualise_map(antinode_positions, puzzle_input)
    return antinode_positions


def generate_antinodes(base_point, vector, num_rows, num_cols):
    current_point = base_point
    while not current_point.is_outside(num_rows, num_cols):
        yield current_point
        current_point = current_point + vector


def part2(puzzle_input):
    num_rows, num_cols = len(puzzle_input), len(puzzle_input[0])
    frequency_dict = get_frequency_dict(puzzle_input)
    antinode_positions = set()
    for frequency in frequency_dict:
        frequency_positions = frequency_dict[frequency]
        for i, position in enumerate(frequency_positions):
            for j in range(i + 1, len(frequency_positions)):
                antenna_one, antenna_two = frequency_positions[i], frequency_positions[j]
                one_to_two_vector = antenna_two - antenna_one
                antinode_positions = antinode_positions.union({antinode for antinode in generate_antinodes(antenna_two, one_to_two_vector, num_rows, num_cols)})
                antinode_positions = antinode_positions.union({antinode for antinode in generate_antinodes(antenna_one, -one_to_two_vector, num_rows, num_cols)})
    # visualise_map(antinode_positions, puzzle_input)
    return antinode_positions


def main():
    puzzle_input = get_input("test_files/prob8_full_input.txt")
    print(f"Solution to part 1 is: {len(part1(puzzle_input))}")
    print(f"Solution to part 2 is: {len(part2(puzzle_input))}")


if __name__ == "__main__":
    main()