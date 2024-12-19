def is_position_outside_map(position, num_rows, num_cols):
    row_pos, col_pos = position
    if (0 <= row_pos < num_rows) and (0 <= col_pos < num_cols):
        return False
    return True


def intify_list(string_list):
    return [int(char) for char in string_list]


def add_vector(x, y):
    return x[0] + y[0], x[1] + y[1]


def get_neighbour_positions(position):
    neighbour_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for direction in neighbour_directions:
        yield position[0] + direction[0], position[1] + direction[1]
