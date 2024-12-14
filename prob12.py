import itertools
from collections import Counter

from util import is_position_outside_map


def get_input(filename):
    with open(filename, "r") as f:
        return [list(line.strip()) for line in f.readlines()]


def get_neighbour_positions(position):
    neighbour_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for direction in neighbour_directions:
        yield position[0] + direction[0], position[1] + direction[1]


def flood_fill(base_point, puzzle_input, num_rows, num_cols):
    region = {base_point}
    region_type = puzzle_input[base_point[0]][base_point[1]]
    visited = set()
    while True:
        region_update = set()
        for position in region - visited:
            for neighbour_position in get_neighbour_positions(position):
                if not is_position_outside_map(neighbour_position, num_rows, num_cols) and neighbour_position not in visited:
                    if region_type == puzzle_input[neighbour_position[0]][neighbour_position[1]]:
                        region_update.add(neighbour_position)
        if region_update == set():
            return region_type, region
        visited = region
        region = region.union(region_update)


def get_perimeter(region):
    edges = Counter()
    for position in region:
        r, c = position[0], position[1]
        position_edges = Counter([
            (r - 0.5, c),
            (r + 0.5, c),
            (r, c - 0.5),
            (r, c + 0.5),
        ])
        edges += position_edges
    return [edge for edge in edges if edges[edge] == 1]


def get_edge_direction_map(region, perimeter):
    edge_plot_map = {}
    for edge in perimeter:
        r, c = edge
        possible_plots = {
            (r - 0.5, c),
            (r + 0.5, c),
            (r, c - 0.5),
            (r, c + 0.5),
        }
        for possible_plot in possible_plots:
            if possible_plot in region:
                edge_plot_map[edge] = (edge[0] - possible_plot[0], edge[1] - possible_plot[1])
    return edge_plot_map


def get_sides(region):
    perimeter_positions = set(get_perimeter(region))
    edge_direction_map = get_edge_direction_map(region, perimeter_positions)
    horizontal_edges = sorted([edge for edge in perimeter_positions if edge[1] % 1 == 0], key=lambda edge: edge[0])
    vertical_edges = sorted([edge for edge in perimeter_positions if edge[0] % 1 == 0], key=lambda edge: edge[1])

    sides = 0
    for _, horizontal_line in itertools.groupby(horizontal_edges, lambda edge: edge[0]):
        horizontal_line = list((sorted(horizontal_line, key=lambda edge: edge[1])))
        if len(horizontal_line) == 1:
            sides += 1
        else:
            for i, current_edge in enumerate(horizontal_line[:-1]):
                next_edge = horizontal_line[i + 1]
                if next_edge[1] - current_edge[1] == 1 and edge_direction_map[next_edge] == edge_direction_map[current_edge]:
                    pass
                else:
                    sides += 1
            sides += 1

    for _, vertical_line in itertools.groupby(vertical_edges, lambda edge: edge[1]):
        vertical_line = list((sorted(vertical_line, key=lambda edge: edge[0])))
        if len(vertical_line) == 1:
            sides += 1
        else:
            for i, current_edge in enumerate(vertical_line[:-1]):
                next_edge = vertical_line[i + 1]
                if next_edge[0] - current_edge[0] == 1 and edge_direction_map[next_edge] == edge_direction_map[current_edge]:
                    pass
                else:
                    sides += 1
            sides += 1

    return sides


def solve(puzzle_input):
    num_rows, num_cols = len(puzzle_input), len(puzzle_input[0])
    unfilled_plots = {(i, j) for i in range(num_rows) for j in range(num_cols)}
    regions_types = []
    part1_price = 0
    part2_price = 0
    while len(unfilled_plots) > 0:
        base_point = next(iter(unfilled_plots))
        region_type, region = flood_fill(base_point, puzzle_input, num_rows, num_cols)
        regions_types.append((region_type, region))
        unfilled_plots -= region
    for region_type, region in regions_types:
        perimeter = get_perimeter(region)
        sides = get_sides(region)
        part1_price += len(region)*len(perimeter)
        part2_price += len(region)*sides
    print(f"{len(regions_types)=}")
    return part1_price, part2_price


def main():
    puzzle_input = get_input("test_files/prob12_full_input.txt")
    part1_solution, part2_solution = solve(puzzle_input)
    print(f"Solution to part 1 is: {part1_solution}")
    print(f"Solution to part 2 is: {part2_solution}")


if __name__ == "__main__":
    main()
