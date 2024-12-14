from typing import List


def get_input(filename) -> List[List[int]]:
    with open(filename, "r") as f:
        return [[int(num) for num in line.split()] for line in f.readlines()]


def is_report_safe(report: List[int]) -> bool:
    if report[1] == report[0]:
        return False
    ascending = report[1] - report[0] > 0
    for i in range(1, len(report)):
        if not (1 <= abs(report[i] - report[i - 1]) <= 3):
            return False
        if ascending:
            if report[i] < report[i - 1]:
                return False
        else:
            if report[i] > report[i - 1]:
                return False
    return True


def part1(reports: List[List[int]]) -> int:
    return len([r for r in reports if is_report_safe(r)])


def is_report_dampener_safe(report: List[int]) -> bool:
    if is_report_safe(report):
        return True
    for i in range(len(report)):
        popped_report = report[:i] + report[i+1:]
        if is_report_safe(popped_report):
            return True
    return False


def part2(reports: List[List[int]]) -> int:
    return len([r for r in reports if is_report_dampener_safe(r)])


def main():
    problem_input = get_input("test_files/prob2_full_input.txt")
    print(f"Part 1 solution is: {part1(problem_input)}")
    print(f"Part 2 solution is: {part2(problem_input)}")


if __name__ == "__main__":
    main()