from util import add_vector, get_map_starting_position


def visualise_maze(maze):
    for line in maze:
        print(line)


def get_maze_char(maze, position):
    return maze[position[0]][position[1]]


def is_position_char(maze, position, char):
    return get_maze_char(maze, position) == char


def get_scores(path, maze, direction, current_score):
    """recursive solution, hits max recursion depth on the full input :("""
    path_endpoint = path[-1]
    if get_maze_char(maze, path_endpoint) == "E":
        return [current_score], [path]
    straight_ahead_step = add_vector(path_endpoint, direction)
    clockwise_direction = [direction[1], -direction[0]]
    anti_clockwise_direction = [-direction[1], direction[0]]
    anti_clockwise_step = add_vector(path_endpoint, anti_clockwise_direction)
    clockwise_step = add_vector(path_endpoint, clockwise_direction)
    new_scores, new_paths = [], []

    for step, step_direction in zip([straight_ahead_step, anti_clockwise_step, clockwise_step], [direction, anti_clockwise_direction, clockwise_direction]):
        if not is_position_char(maze, step, "#") and step not in path:
            if step_direction == direction:
                score_update = 1
            else:
                score_update = 1001
            new_path = path + [step]
            scores, paths = get_scores(new_path, maze, step_direction, current_score)
            new_scores += [score + score_update for score in scores]
            new_paths += paths
    return new_scores, new_paths


class Path:
    def __init__(self, path, score, direction):
        self.path = path
        self.score = score
        self.direction = direction

    def __repr__(self):
        return f"Path({self.path}, {self.score}, {self.direction})"


def visualise(maze, positions):
    path_lines = []
    for i, line in enumerate(maze):
        path_line = ""
        for j in range(len(line)):
            if (i, j) in positions:
                path_line += "O"
            else:
                path_line += maze[i][j]
        path_lines.append(path_line)
    for line in path_lines:
        print(line)


def part1(maze, starting_position):
    # scores, paths = get_scores([starting_position], maze, [0, 1], 0)
    # print(f"Recursive solution to part 1 is: {min(scores)}")

    paths = [Path([starting_position], 0, [0, 1])]
    finished_paths = []
    maze_cache = {}
    while len(paths) > 0:
        # print(len(paths))
        new_paths = []
        for path in paths:
            path_endpoint = path.path[-1]
            cache_key = (path_endpoint, tuple(path.direction))
            if not ((cache_key in maze_cache) and maze_cache[cache_key] < path.score):
                maze_cache[cache_key] = path.score
                straight_ahead_step = add_vector(path_endpoint, path.direction)
                clockwise_direction = [path.direction[1], -path.direction[0]]
                anti_clockwise_direction = [-path.direction[1], path.direction[0]]
                anti_clockwise_step = add_vector(path_endpoint, anti_clockwise_direction)
                clockwise_step = add_vector(path_endpoint, clockwise_direction)
                for next_step, next_direction in zip([straight_ahead_step, anti_clockwise_step, clockwise_step], [path.direction, anti_clockwise_direction, clockwise_direction]):
                    if not is_position_char(maze, next_step, "#") and next_step not in path.path:
                        if next_step == straight_ahead_step:
                            new_path = Path(path.path + [next_step], path.score + 1, next_direction)
                        else:
                            new_path = Path(path.path + [next_step], path.score + 1001, next_direction)
                        if is_position_char(maze, next_step, "E"):
                            finished_paths.append(new_path)
                        else:
                            new_paths.append(new_path)
        paths = new_paths
    best_score = min([path.score for path in finished_paths])
    print(f"Solution to part 1 is {best_score}")
    best_paths = [path for path in finished_paths if path.score == best_score]
    best_path_positions = {position for path in best_paths for position in path.path}
    # visualise(maze, best_path_positions)
    print(f"Solution to part 2 is {len(best_path_positions)}")


def main():
    maze, starting_position = get_map_starting_position("test_files/prob16_full_input.txt")
    part1(maze, starting_position)


if __name__ == "__main__":
    main()

