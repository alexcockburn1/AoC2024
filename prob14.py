import math
import re
from collections import Counter

import numpy as np

from util import intify_list


def get_input(filename):
    # p=0,4 v=3,-3
    pattern = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    positions_velocities = []
    with open(filename, "r") as f:
        for line in f.readlines():
            px, py, vx, vy = intify_list(re.findall(pattern, line)[0])
            positions_velocities.append([np.array([py, px]), np.array([vy, vx])])
    return positions_velocities


def visualise_robots(robots, row_num, col_num):
    lines = []
    robot_positions = aggregate_robot_positions(robots)
    for i in range(row_num):
        line = ""
        for j in range(col_num):
            if (i, j) in robot_positions:
                line += (str(robot_positions[(i, j)]))
            else:
                line += "."
        lines.append(line)
    for line in lines:
        print(line)
    print("\n")


def aggregate_robot_positions(robots):
    return Counter([(position[0], position[1]) for position, _ in robots])


def get_quadrant_scores(aggregated_robots, col_num, row_num):
    mid_row, mid_col = row_num // 2, col_num // 2
    upper_left_total = sum([aggregated_robots[position] for position in aggregated_robots if
                            position[0] < mid_row and position[1] < mid_col])
    upper_right_total = sum([aggregated_robots[position] for position in aggregated_robots if
                             position[0] < mid_row and position[1] > mid_col])
    lower_left_total = sum([aggregated_robots[position] for position in aggregated_robots if
                            position[0] > mid_row and position[1] < mid_col])
    lower_right_total = sum([aggregated_robots[position] for position in aggregated_robots if
                             position[0] > mid_row and position[1] > mid_col])
    return [lower_left_total, lower_right_total, upper_left_total, upper_right_total]


def get_safety_factor(aggregated_robots, row_num, col_num):
    lower_left_total, lower_right_total, upper_left_total, upper_right_total = get_quadrant_scores(aggregated_robots,
                                                                                                   col_num, row_num)
    return upper_left_total*upper_right_total*lower_left_total*lower_right_total


def part1(robots, row_num, col_num, time_steps):
    quadrant_maxes = [0]*4
    for time_step in range(time_steps):
        new_robots = []
        for robot in robots:
            robot_position, robot_velocity = robot
            new_robot_position = robot_position + robot_velocity
            new_robot_position[0] = new_robot_position[0] % row_num
            new_robot_position[1] = new_robot_position[1] % col_num
            new_robots.append([new_robot_position, robot_velocity])
        robots = new_robots
        aggregated_robots = aggregate_robot_positions(robots)
        quadrant_scores = get_quadrant_scores(aggregated_robots, row_num, col_num)
        for i in range(len(quadrant_scores)):
            if quadrant_scores[i] > quadrant_maxes[i]:
                quadrant_maxes[i] = quadrant_scores[i]
        if quadrant_scores[3] == 339:
            visualise_robots(robots, row_num, col_num)
            print(f"Found xmas tree after {time_step + 1} steps!")
        # print(f"{num_aggregated_robots=}")
    # visualise_robots(robots, row_num, col_num)
    print(quadrant_maxes)
    return get_safety_factor(aggregated_robots, row_num, col_num)


def main():
    # robots = get_input("test_files/prob14_test_input.txt")
    # col_num, row_num = 11, 7
    robots = get_input("test_files/prob14_full_input.txt")
    col_num, row_num = 101, 103
    # print(robots, row_num, col_num)
    safety_factor = part1(robots, row_num, col_num, 10000)
    print(f"Solution to part 1 is: {safety_factor}")


if __name__ == "__main__":
    main()

