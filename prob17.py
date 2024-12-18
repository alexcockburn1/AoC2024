import math


def get_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        a_value = int(lines[0].replace("Register A:", ""))
        b_value = int(lines[1].replace("Register B:", ""))
        c_value = int(lines[2].replace("Register C:", ""))

        program = [int(char) for char in lines[4].replace("Program: ", "").split(",")]

        return a_value, b_value, c_value, program


def run_program(parsed_input):
    a_value, b_value, c_value, program = parsed_input
    pc = 0

    def get_combo_operand(num):
        if 0 <= num <= 3:
            return num
        elif num == 4:
            return a_value
        elif num == 5:
            return b_value
        elif num == 6:
            return c_value

    while pc < len(program):
        op = program[pc]
        operand = program[pc + 1]
        # print(f"{op_dict[op]=}, {operand=}, {get_combo_operand(operand)=}, {a_value=}, {b_value=}, {c_value=}")
        jump = True
        if op == 0:
            a_value = int(a_value / 2**get_combo_operand(operand))
        elif op == 1:
            b_value = b_value^operand
        elif op == 2:
            b_value = get_combo_operand(operand) % 8
        elif op == 3:
            if a_value != 0:
                pc = operand
                jump = False
        elif op == 4:
            b_value = b_value ^ c_value
        elif op == 5:
            yield get_combo_operand(operand) % 8
        elif op == 6:
            b_value = int(a_value / 2 ** get_combo_operand(operand))
        elif op == 7:
            c_value = int(a_value / 2 ** get_combo_operand(operand))

        if jump:
            pc += 2


def step(a_value):
    b_value = a_value % 8  # 2,4
    b_value = 1 ^ b_value  # 1,1
    c_value = math.floor(a_value / 2 ** b_value)  # 7,5
    a_value = math.floor(a_value / 8)  # 0,3
    b_value = 4 ^ b_value  # 1,4
    b_value = b_value ^ c_value  # 4, 0
    return b_value % 8, a_value  # 5,5


def part2(parsed_input):
    _, b_value, c_value, program = parsed_input
    a_values = {0}
    for program_val in program[::-1]:
        new_a_values = set()
        for a_value in a_values:
            for previous_a_val in range(8*a_value, 8*a_value + 8):
                out, _ = step(previous_a_val)
                if out == program_val:
                    new_a_values.add(previous_a_val)
        a_values = new_a_values
    return min(a_values)


def main():
    parsed_input = get_input("test_files/prob17_full_input.txt")
    print(parsed_input)
    out = list(run_program(parsed_input))
    outstr = ",".join([str(num) for num in out])
    print(f"Solution to part 1 is {outstr}")
    min_val = part2(parsed_input)
    print(f"Solution to part 2 is {min_val}")


if __name__ == "__main__":
    main()