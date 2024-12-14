from util import is_position_outside_map


def get_input(filename):
    with open(filename, "r") as f:
        return [[int(char) if char != "." else char for char in line.strip()] for line in f.readlines()]


def get_starts(puzzle_input):
    starts = []
    for i, line in enumerate(puzzle_input):
        for j in range(len(puzzle_input[i])):
            if puzzle_input[i][j] == 0:
                starts.append((i, j))
    return starts


def get_uphill_neighbours(position, num_rows, num_cols, puzzle_input):
    neighbour_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for direction in neighbour_directions:
        neighbour_position = (position[0] + direction[0], position[1] + direction[1])
        current_val = puzzle_input[position[0]][position[1]]
        if not is_position_outside_map(neighbour_position, num_rows, num_cols):
            neighbour_val = puzzle_input[neighbour_position[0]][neighbour_position[1]]
            if neighbour_val == current_val + 1:
                yield neighbour_position, neighbour_val


def get_total_score(current_position, current_trail_ends, num_rows, num_cols, puzzle_input):
    # print(f"{current_position=}")
    current_val = puzzle_input[current_position[0]][current_position[1]]
    if current_val == 9:
        # print(f"Encountered recursion exit at {current_position}")
        current_trail_ends = current_trail_ends.union({current_position})
        return current_trail_ends, 1
    recursed_trails_count = set()
    current_rating = 0
    for neighbour_position, neighbour_val in get_uphill_neighbours(current_position, num_rows, num_cols, puzzle_input):
        score, rating = get_total_score(neighbour_position, current_trail_ends, num_rows, num_cols, puzzle_input)
        current_rating += rating
        recursed_trails_count = recursed_trails_count.union(score)
    return current_trail_ends.union(recursed_trails_count), current_rating


def solve(puzzle_input):
    starts = get_starts(puzzle_input)
    num_rows = len(puzzle_input)
    num_cols = len(puzzle_input[0])
    all_trail_ends = []
    ratings = []
    for start in starts:
        trail_ends = set()
        final_score, final_rating = get_total_score(start, trail_ends, num_rows, num_cols, puzzle_input)
        all_trail_ends.append(final_score)
        ratings.append(final_rating)
    # print(all_trail_ends)
    # print([len(trail_ends) for trail_ends in all_trail_ends])
    return sum([len(trail_ends) for trail_ends in all_trail_ends]), sum(ratings)


def main():
    puzzle_input = get_input("test_files/prob10_full_input.txt")
    part1_solution, part2_solution = solve(puzzle_input)
    print(f"Solution to part 1 is {part1_solution}")
    print(f"Solution to part 1 is {part2_solution}")


if __name__ == "__main__":
    main()
