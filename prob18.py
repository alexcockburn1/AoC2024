import math
from collections import defaultdict

from util import get_neighbour_positions, is_position_outside_map


def get_input(filename):
    positions = []
    with open(filename, "r") as f:
        for line in f.readlines():
            x, y = [int(num) for num in line.strip().split(",")]
            positions.append((y, x))
    return positions


def get_neighbours(position, space_size):
    for neighbour in get_neighbour_positions(position):
        if not is_position_outside_map(neighbour, space_size, space_size):
            yield neighbour


def dijkstra(walls, space_size, endpoint):
    walls = set(walls)
    unvisited_set = set()
    distances = {}
    previous_nodes = defaultdict(set)
    for i in range(space_size):
        for j in range(space_size):
            unvisited_set.add((i, j))
            distances[(i, j)] = 0 if (i, j) == (0, 0) else math.inf
    while len(unvisited_set) > 0:
        min_unvisited_value = min([distances[node] for node in unvisited_set])
        min_unvisited_nodes = {node for node in unvisited_set if distances[node] == min_unvisited_value}
        current_position = next(iter(min_unvisited_nodes))
        unvisited_set -= {current_position}
        if current_position == endpoint:
            return distances[current_position], previous_nodes
        for neighbour in get_neighbours(current_position, space_size):
            if neighbour not in walls and neighbour in unvisited_set:
                updated_distance = distances[current_position] + 1
                if updated_distance < distances[neighbour]:
                    distances[neighbour] = updated_distance
                    previous_nodes[neighbour] = {current_position}
                elif updated_distance == distances[neighbour]:
                    previous_nodes[neighbour].add(current_position)


def check_can_reach_endpoint(startpoint, endpoint, walls, space_size):
    walls = set(walls)
    region = {startpoint}
    visited = set()
    while True:
        region_update = set()
        for position in region - visited:
            for neighbour in get_neighbours(position, space_size):
                if neighbour not in walls:
                    if neighbour == endpoint:
                        return True
                    if neighbour not in visited:
                        region_update.add(neighbour)
        if region_update == set():
            return False
        visited = region
        region = region.union(region_update)


def main():
    walls = get_input("test_files/prob18_full_input.txt")
    space_size = 71
    startpoint = (0, 0)
    endpoint = (space_size - 1, space_size - 1)
    initial_wall_limit = 1024
    best_distance, previous_nodes = dijkstra(set(walls[:initial_wall_limit]), space_size, endpoint)
    print(f"Solution to part 1 is {best_distance}")
    for i in range(initial_wall_limit + 1, len(walls)):
        if i % 10 == 0:
            print(f"{i=}")
        if not check_can_reach_endpoint(startpoint, endpoint, set(walls[:i+1]), space_size):
            y, x = walls[i]
            print(f"Solution to part 2 is {(x, y)}")
            break


if __name__ == "__main__":
    main()