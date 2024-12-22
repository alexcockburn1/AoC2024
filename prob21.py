import math
from collections import defaultdict

from util import get_neighbour_positions, sub_vector


def get_codes(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]


def get_neighbours(position, space):
    for neighbour in get_neighbour_positions(position):
        if neighbour in space:
            yield neighbour


def dijkstra(startpoint, endpoint, space):
    unvisited_set = space.copy()
    distances = {}
    previous_nodes = defaultdict(set)
    for point in space:
        distances[point] = 0 if point == startpoint else math.inf
    while len(unvisited_set) > 0:
        min_unvisited_value = min([distances[node] for node in unvisited_set])
        min_unvisited_nodes = {node for node in unvisited_set if distances[node] == min_unvisited_value}
        current_position = next(iter(min_unvisited_nodes))
        unvisited_set -= {current_position}
        if current_position == endpoint:
            return distances[current_position], previous_nodes
        for neighbour in get_neighbours(current_position, space):
            if neighbour in unvisited_set:
                updated_distance = distances[current_position] + 1
                if updated_distance < distances[neighbour]:
                    distances[neighbour] = updated_distance
                    previous_nodes[neighbour] = {current_position}
                elif updated_distance == distances[neighbour]:
                    previous_nodes[neighbour].add(current_position)


def path_to_directions(path):
    direction_map = {
        (1, 0): "v",
        (-1, 0): "^",
        (0, 1): ">",
        (0, -1): "<"
    }
    direction_string = ""
    for i in range(1, len(path)):
        direction = sub_vector(path[i], path[i - 1])
        direction_string += direction_map[direction]
    return direction_string


def get_paths(startpoint, endpoint, previous_nodes):
    paths = [[endpoint]]
    while set({path[-1] for path in paths}) != {startpoint}:
        next_paths = []
        for path in paths:
            for prev_node in previous_nodes[path[-1]]:
                next_paths.append(path + [prev_node])
        paths = next_paths
    return [path_to_directions(list(reversed(path))) for path in paths]


def get_key_to_arrow_map(space):
    keypad_map = {}
    for startpoint in space:
        for endpoint in space:
            distances, previous_nodes = dijkstra(startpoint, endpoint, space)
            paths = get_paths(startpoint, endpoint, previous_nodes)
            keypad_map[(startpoint, endpoint)] = paths
    return keypad_map


key_to_position = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2), "1": (2, 0), "2": (2, 1), "3": (2, 2), "0": (3, 1), "A": (3, 2)
}

direction_to_position = {
    "^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)
}


def get_button_presses(target_keys, keypad_map, a_position, key_position_map):
    current_position = a_position
    button_presses_list = [""]
    for char in target_keys:
        char_pos = key_position_map[char]
        button_presses_list = [button_presses + presses + "A" for button_presses in button_presses_list for presses in
                               keypad_map[(current_position, char_pos)]]
        current_position = char_pos
    return button_presses_list


def get_next_best_paths(paths_map, space, best_paths):
    next_best_paths = {}
    for start in space:
        for end in space:
            paths = paths_map[(start, end)]
            min_value = math.inf
            for path in paths:
                path_sum = 0
                path = "A" + path + "A"
                for char, next_char in zip(path, path[1:]):
                    path_sum += best_paths[(direction_to_position[char], direction_to_position[next_char])]
                if path_sum < min_value:
                    min_value = path_sum
            next_best_paths[(start, end)] = min_value
    return next_best_paths


def part2():
    codes = get_codes("test_files/prob21_full_input.txt")
    keypad_space = set(key_to_position.values())
    arrow_space = set(direction_to_position.values())
    keypad_map = get_key_to_arrow_map(keypad_space)
    arrow_map = get_key_to_arrow_map(arrow_space)
    best_paths = {start_end: 1 for start_end in arrow_map.keys()}
    for _ in range(25):
        best_paths = get_next_best_paths(arrow_map, arrow_space, best_paths)
    best_paths = get_next_best_paths(keypad_map, keypad_space, best_paths)
    total_complexity = 0
    for code in codes:
        code = "A" + code
        min_length = 0
        for char, next_char in zip(code, code[1:]):
            min_length += best_paths[(key_to_position[char], key_to_position[next_char])]
        total_complexity += min_length*int(code[1:4])
    print(f"Solution to part 2 is {total_complexity}")


def part1():
    codes = get_codes("test_files/prob21_test_input.txt")
    keypad_space = set(key_to_position.values())
    arrow_space = set(direction_to_position.values())
    keypad_map = get_key_to_arrow_map(keypad_space)
    arrow_map = get_key_to_arrow_map(arrow_space)
    total_complexity = 0
    for code in codes:
        print(code)
        button_presses_list = get_button_presses(code, keypad_map, (3, 2), key_to_position)
        for _ in range(2):
            button_presses_list = [new_button_presses for button_presses in button_presses_list for new_button_presses in get_button_presses(button_presses, arrow_map, (0, 2), direction_to_position)]
            print(len(button_presses_list))
        total_complexity += min([len(button_presses) for button_presses in button_presses_list])*int(code[:3])
    print(f"Solution to part 1 is {total_complexity}")


if __name__ == "__main__":
    part1()
    part2()
