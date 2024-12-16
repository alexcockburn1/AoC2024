import numpy as np

from util import add_vector

direction_map = {"^": [-1, 0],
                 ">": [0, 1],
                 "<": [0, -1],
                 "v": [1, 0]}


def get_input(filename):
    map_lines = []
    direction_lines = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            if "#" in line:
                map_lines.append(list(line.strip()))
            elif any([direction in line for direction in direction_map]):
                direction_lines += line.strip()
    return map_lines, direction_lines


def visualise_map(input_map):
    outstring = ""
    for line in input_map:
        outstring += "".join(line) + "\n"
    print(outstring)


def push_stones(input_map, current_position, direction):
    if direction == "^":
        push_slice = input_map[0:current_position[0] + 1, current_position[1]][::-1]
    elif direction == "v":
        push_slice = input_map[current_position[0]:, current_position[1]]
    elif direction == "<":
        push_slice = input_map[current_position[0], 0:current_position[1] + 1][::-1]
    elif direction == ">":
        push_slice = input_map[current_position[0], current_position[1]:]

    block_end = None
    for i in range(1, len(push_slice)):
        if push_slice[i] == "#":
            return block_end
        elif push_slice[i] == ".":
            block_end = i
            break

    if block_end:
        push_slice = np.concatenate((["."], ["@"], ["O"]*(block_end - 1), push_slice[block_end + 1:]))

    if direction == "^":
        input_map[0:current_position[0] + 1, current_position[1]] = push_slice[::-1]
    elif direction == "v":
        input_map[current_position[0]:, current_position[1]] = push_slice
    elif direction == "<":
        input_map[current_position[0], 0:current_position[1] + 1] = push_slice[::-1]
    elif direction == ">":
        input_map[current_position[0], current_position[1]:] = push_slice
    return block_end


def get_score(input_map):
    o_positions = np.where(input_map == "O")
    return sum(100*o_positions[0] + o_positions[1])


def part1(input_map, directions):
    input_map = np.array(input_map)
    current_position = np.where(input_map == "@")
    current_position = np.array([current_position[0][0], current_position[1][0]])
    for direction in directions:
        next_position = current_position + direction_map[direction]
        next_char = input_map[next_position[0]][next_position[1]]
        if next_char == "#":
            pass
        elif next_char == ".":
            input_map[next_position[0]][next_position[1]] = "@"
            input_map[current_position[0]][current_position[1]] = "."
            current_position = next_position
        else:
            block_end = push_stones(input_map, current_position, direction)
            if block_end:
                current_position = next_position
        # print(f"After move {direction}")
    visualise_map(input_map)
    score = get_score(input_map)
    print(f"Solution to part 1 is {score}")


def visualise_part2_map(wall_only_map, sides, current_position):
    outstring = ""
    sides
    for row_num, line in enumerate(wall_only_map):
        out_line = ""
        for col_num in range(len(line)):
            if (row_num, col_num) in sides:
                out_line += sides[(row_num, col_num)][1]
            elif (row_num, col_num) == current_position:
                out_line += "@"
            else:
                out_line += wall_only_map[row_num][col_num]
        outstring += out_line
        outstring += "\n"
    print(outstring)


def expand_parse_map(input_map):
    walls_only_map = []
    boxes = {}
    current_position = None
    for row_num, line in enumerate(input_map):
        walls_only_line = []
        for col_num in range(len(line)):
            if line[col_num] == "#":
                walls_only_line += "##"
            elif line[col_num] == "O":
                boxes[(row_num, 2*col_num)] = ((row_num, 2*col_num + 1), "[")
                boxes[(row_num, 2*col_num + 1)] = ((row_num, 2*col_num), "]")
                walls_only_line += ".."
            elif line[col_num] == "@":
                current_position = (row_num, 2*col_num)
                walls_only_line += ".."
            else:
                walls_only_line += ".."
        walls_only_map.append(walls_only_line)
    visualise_map(walls_only_map)
    visualise_part2_map(walls_only_map, boxes, current_position)
    return walls_only_map, boxes, current_position


def get_side_tree(direction_vector, sides, walls_only_map, tree):
    while True:
        leaves = tree[-1]
        next_layer = set()
        for side in leaves:
            possible_side = add_vector(side, direction_vector)
            if walls_only_map[possible_side[0]][possible_side[1]] == "#":
                return None
            elif possible_side in sides:
                next_layer = next_layer.union({possible_side, sides[possible_side][0]})
        if next_layer == set():
            return tree
        tree.append(next_layer)


def get_new_sides(direction_vector, side_block, sides):
    new_sides = {}
    for side in sides:
        if side in side_block:
            new_sides[add_vector(side, direction_vector)] = (
                add_vector(sides[side][0], direction_vector), sides[side][1])
        else:
            new_sides[side] = sides[side]
    return new_sides


def get_box_score(sides):
    total = 0
    for side in sides:
        if sides[side][1] == "[":
            total += 100*side[0] + side[1]
    return total


def part2(input_map, directions):
    walls_only_map, sides, current_position = expand_parse_map(input_map)
    for direction in directions:
        direction_vector = direction_map[direction]
        next_position = add_vector(current_position, direction_vector)
        next_wall_char = walls_only_map[next_position[0]][next_position[1]]
        if next_wall_char == "#":
            continue
        elif next_position in sides:
            if direction in {">", "<"}:
                side_block = []
                walk_position = next_position
                while walk_position in sides:
                    side_block.append(walk_position)
                    walk_position = add_vector(walk_position, direction_vector)
                if not walls_only_map[walk_position[0]][walk_position[1]] == "#":
                    sides = get_new_sides(direction_vector, side_block, sides)
                    current_position = next_position
            else:
                root = [{next_position, sides[next_position][0]}]
                side_tree = get_side_tree(direction_vector, sides, walls_only_map, root)
                if side_tree:
                    side_block = {side for layer in side_tree for side in layer}
                    sides = get_new_sides(direction_vector, side_block, sides)
                    current_position = next_position
        else:
            current_position = next_position
        # print(f"After move {direction}")
        # visualise_part2_map(walls_only_map, sides, current_position)
    score = get_box_score(sides)
    print(f"Solution to part 2 is {score}")


def main():
    input_map, directions = get_input("test_files/prob15_full_input.txt")
    part1(input_map, directions)
    part2(input_map, directions)


    if __name__ == "__main__":
        main()

