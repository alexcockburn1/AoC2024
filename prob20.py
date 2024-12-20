from collections import Counter

from util import get_map_starting_position, get_val_at_position, get_neighbour_positions, is_position_outside_map, \
    NEIGHBOUR_DIRECTIONS, add_vector


def get_path_dict(num_cols, num_rows, puzzle_map, starting_position):
    current_position = starting_position
    path_dict = {current_position: 0}
    while get_val_at_position(puzzle_map, current_position) != "E":
        for possible_next in get_neighbour_positions(current_position):
            if not is_position_outside_map(possible_next, num_rows, num_cols):
                if possible_next not in path_dict and not get_val_at_position(puzzle_map, possible_next) == "#":
                    path_dict[possible_next] = path_dict[current_position] + 1
                    current_position = possible_next
    return path_dict


def part1(puzzle_map, starting_position):
    num_rows, num_cols = len(puzzle_map), len(puzzle_map[0])
    path_dict = get_path_dict(num_cols, num_rows, puzzle_map, starting_position)

    good_cheats = 0

    cheat_counter = Counter()
    for position in path_dict:
        for direction in NEIGHBOUR_DIRECTIONS:
            cheat1 = add_vector(position, direction)
            if get_val_at_position(puzzle_map, cheat1) == "#":
                possible_cheat2 = add_vector(cheat1, direction)
                if possible_cheat2 in path_dict and path_dict[possible_cheat2] > path_dict[position]:
                    cheat_saving = path_dict[possible_cheat2] - path_dict[position] - 2
                    if cheat_saving >= 100:
                        cheat_counter[cheat_saving] += 1
                        good_cheats += 1
    for k, v in sorted(cheat_counter.items(), key=lambda x: x[0]):
        print(f"Found {v} cheats saving {k} picoseconds")
    print(f"solution to part 1 is {good_cheats}")


def get_possible_cheats(puzzle_map, position, cheat_size, num_rows, num_cols, path_dict):
    for row_offset in range(-cheat_size, cheat_size + 1):
        for col_offset in range(-(cheat_size - abs(row_offset)), (cheat_size - abs(row_offset)) + 1):
            cheat = add_vector(position, (row_offset, col_offset))
            if not is_position_outside_map(cheat, num_rows, num_cols) and not get_val_at_position(puzzle_map,
                                                                                                  cheat) == "#":
                if cheat in path_dict and path_dict[cheat] > path_dict[position]:
                    cheat_saving = path_dict[cheat] - path_dict[position] - abs(row_offset) - abs(col_offset)
                    yield cheat, cheat_saving


def part2(puzzle_map, starting_position):
    num_rows, num_cols = len(puzzle_map), len(puzzle_map[0])
    cheat_counter = Counter()
    path_dict = get_path_dict(num_cols, num_rows, puzzle_map, starting_position)
    for position in path_dict:
        for cheat, cheat_saving in get_possible_cheats(puzzle_map, position, 20, num_rows, num_cols, path_dict):
            if cheat_saving >= 100:
                cheat_counter[cheat_saving] += 1
    for k, v in sorted(cheat_counter.items(), key=lambda x: x[0]):
        print(f"Found {v} cheats saving {k} picoseconds")
    print(f"Solution to part 2 is {sum(cheat_counter.values())}")


def main():
    puzzle_map, starting_position = get_map_starting_position("test_files/prob20_full_input.txt")
    part1(puzzle_map, starting_position)
    part2(puzzle_map, starting_position)


if __name__ == "__main__":
    main()
