from util import is_position_outside_map


def get_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        for i, line in enumerate(lines):
            if "^" in line:
                starting_position = i, line.index("^")
        return starting_position, lines


def visualise_route(positions, puzzle_map):
    for i, line in enumerate(puzzle_map):
        line_to_print = list(line)
        for j in range(len(line)):
            if (i, j) in positions:
                line_to_print[j] = "X"
        print("".join(line_to_print))


def turn_right(direction):
    return direction[1], -direction[0]


def walk(num_cols, num_rows, puzzle_map, starting_position, starting_direction):
    position = starting_position
    direction = starting_direction
    while True:
        yield position, direction
        position_in_front = (position[0] + direction[0], position[1] + direction[1])
        if is_position_outside_map(position_in_front, num_rows, num_cols):
            break
        if puzzle_map[position_in_front[0]][position_in_front[1]] == "#":
            direction = turn_right(direction)
        else:
            position = position_in_front


def part1(num_cols, num_rows, puzzle_map, starting_position, starting_direction):
    step_generator = walk(num_cols, num_rows, puzzle_map, starting_position, starting_direction)
    return {position for position, _ in step_generator}


def update_map(original_map, update_position):
    row_num, col_num = update_position
    updated_map = []
    for i, line in enumerate(original_map):
        if i == row_num:
            updated_map.append(line[:col_num] + "#" + line[col_num + 1:])
        else:
            updated_map.append(line)
    return updated_map


def part2_easier(num_cols, num_rows, puzzle_map, starting_position, possible_obstacle_places):
    starting_direction = (-1, 0)
    good_obstacles = set()
    walk_counter = 0
    for possible_obstacle_place in possible_obstacle_places:
        print(f"{walk_counter=}")
        walk_counter += 1
        updated_map = update_map(puzzle_map, possible_obstacle_place)
        positions_directions = set()
        walk_with_obstacle = walk(num_cols, num_rows, updated_map, starting_position, starting_direction)
        for position_direction in walk_with_obstacle:
            if position_direction in positions_directions:
                good_obstacles.add(possible_obstacle_place)
                break
            else:
                positions_directions.add(position_direction)
    return good_obstacles


def main():
    starting_position, puzzle_map = get_input("test_files/prob6_full_input.txt")
    num_rows = len(puzzle_map)
    num_cols = len(puzzle_map[0])
    starting_direction = (-1, 0)
    positions = part1(num_cols, num_rows, puzzle_map, starting_position, starting_direction)
    print(f"Solution to part 1 is {len(positions)}")

    # visualise_route(positions, puzzle_map)
    possible_obstacles = positions - {starting_position}
    good_obstacles = part2_easier(num_cols, num_rows, puzzle_map, starting_position, possible_obstacles)
    print(good_obstacles)
    print(f"Solution to part 2 is: {len(good_obstacles)}")


if __name__ == "__main__":
    main()