import re

from util import intify_list


def is_probably_int(num):
    return abs(num - round(num)) < 0.000000001


def get_input(filename):
    button_regex = r"Button .: X\+(\d+), Y\+(\d+)"
    prize_regex = r"Prize: X=(\d+), Y=(\d+)"
    parsed_input = []
    with open(filename) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            button_a_line, button_b_line, prize_line = lines[i], lines[i+1], lines[i+2]
            a_vector = intify_list(re.findall(button_regex, button_a_line)[0])
            b_vector = intify_list(re.findall(button_regex, button_b_line)[0])
            prize_vector = intify_list(re.findall(prize_regex, prize_line)[0])
            parsed_input.append([a_vector, b_vector, prize_vector])
    return parsed_input


def get_min_tokens_part1(machine):
    a, b, p = machine
    det = a[0]*b[1] - a[1]*b[0]
    if det == 0:
        print("    Singular matrix!")
    else:
        print("    Non-singular matrix")
        matrix_inverse = [[b[1]/det, -b[0]/det], [-a[1]/det, a[0]/det]]
        n_a = matrix_inverse[0][0]*p[0] + matrix_inverse[0][1]*p[1]
        n_b = matrix_inverse[1][0]*p[0] + matrix_inverse[1][1]*p[1]
        print(f"    {n_a=},{n_b=}")
        if is_probably_int(n_a) and is_probably_int(n_b):
            n_a, n_b = round(n_a), round(n_b)
            if 0 <= n_a <= 100 and 0 <= n_b <= 100:
                return 3*n_a + n_b
    return 0


def get_min_tokens_no_part2(machine):
    a, b, p = machine
    p = [elem + 10000000000000 for elem in p]
    det = a[0]*b[1] - a[1]*b[0]
    if det == 0:
        print("    Singular matrix!")
    else:
        print("    Non-singular matrix")
        matrix_conjugate = [[b[1], -b[0]], [-a[1], a[0]]]
        det_scaled_n_a = matrix_conjugate[0][0] * p[0] + matrix_conjugate[0][1] * p[1]
        det_scaled_n_b = matrix_conjugate[1][0] * p[0] + matrix_conjugate[1][1] * p[1]
        if det_scaled_n_a % det == 0 and det_scaled_n_b % det == 0:
            n_a, n_b = round(det_scaled_n_a/det), round(det_scaled_n_b/det)
            return 3 * n_a + n_b
    return 0


def part1(puzzle_input):
    total = 0
    for machine in puzzle_input:
        print(f"{machine=}")
        min_cost = get_min_tokens_no_part2(machine)
        total += min_cost
        print(f"    {min_cost=}")
    return total


def part2(puzzle_input):
    total = 0
    for machine in puzzle_input:
        print(f"{machine=}")
        min_cost = get_min_tokens_no_part2(machine)
        total += min_cost
        print(f"    {min_cost=}")
    return total


def main():
    puzzle_input = get_input("test_files/prob13_full_input.txt")
    # print(f"Solution to part 1 is {part1(puzzle_input)}")
    print(f"Solution to part 2 is {part2(puzzle_input)}")


if __name__ == "__main__":
    main()
