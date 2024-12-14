def get_input(filename):
    with open(filename, "r") as f:
        input_lines = []
        for line in f.readlines():
            result, operands_string = line.split(": ")
            operands = operands_string.split(" ")
            input_lines.append((int(result), [int(operand) for operand in operands]))
        return input_lines


def is_satisfiable(result, current_total, remaining_operands, include_concat=False):
    if len(remaining_operands) == 0:
        if result == current_total:
            return True
        return None
    popped_operand, popped_remaining = remaining_operands[0], remaining_operands[1:]
    if is_satisfiable(result, current_total + popped_operand, popped_remaining):
        return True
    if is_satisfiable(result, current_total * popped_operand, popped_remaining):
        return True
    if is_satisfiable(result, int(str(current_total) + str(popped_operand)), popped_remaining):
        return True
    return False


def part1(input_lines):
    total_calibration = 0
    for result, operands in input_lines:
        # print((result, operands), is_satisfiable(result, operands[0], operands[1:]))
        if is_satisfiable(result, operands[0], operands[1:]):
            total_calibration += result
    return total_calibration


def part2(input_lines):
    total_calibration = 0
    for result, operands in input_lines:
        print((result, operands), is_satisfiable(result, operands[0], operands[1:], include_concat=True))
        if is_satisfiable(result, operands[0], operands[1:], include_concat=True):
            total_calibration += result
    return total_calibration


def main():
    input_lines = get_input("test_files/prob7_full_input.txt")
    # print(f"Solution to part 1 is: {part1(input_lines)}")
    print(f"Solution to part 2 is: {part2(input_lines)}")


if __name__ == "__main__":
    main()