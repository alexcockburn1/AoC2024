import itertools
import re
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Gate:
    operand1: Optional[str]
    operator: Optional[str]
    operand2: Optional[str]
    gate_id: str
    value: int = None

    def calculate(self, gate_dict):
        if self.value:
            return self.value
        else:
            if self.operator == "AND":
                self.value = gate_dict[self.operand1].calculate(gate_dict) and gate_dict[self.operand2].calculate(gate_dict)
            elif self.operator == "OR":
                self.value = gate_dict[self.operand1].calculate(gate_dict) or gate_dict[self.operand2].calculate(gate_dict)
            elif self.operator == "XOR":
                self.value = gate_dict[self.operand1].calculate(gate_dict) ^ gate_dict[self.operand2].calculate(gate_dict)
            return self.value


def get_input(filename):
    with open(filename, "r") as f:
        gate_pattern = r"(.*) (AND|OR|XOR) (.*) -> (.*)"
        gate_dict = {}
        for line in f.readlines():
            if ":" in line:
                wire, val = line.split(": ")
                gate_dict[wire] = Gate(None, None, None, wire, int(val))
            elif re.match(gate_pattern, line):
                groups = re.findall(gate_pattern, line)[0]
                gate = Gate(groups[0], groups[1], groups[2], groups[3])
                gate_dict[gate.gate_id] = gate
        return gate_dict


def part1(gate_dict):
    z_values = []
    for gate_id in gate_dict:
        if gate_id.startswith("z"):
            z_values.append((gate_id, gate_dict[gate_id].calculate(gate_dict)))
    z_values = sorted(z_values)
    binary = ""
    for _, val in z_values:
        binary = str(val) + binary
    decimal_out = int(binary, 2)
    print(f"Solution to part 1 is {decimal_out}")


def pad_zero(num):
    num = str(num)
    return "0" + num if len(num) == 0 else num


# def part2(gate_dict):
#     full_adder_size = len([id for id in gate_dict if id.startswith("z")])
#     print(full_adder_size)
#     current_adder_size = 0
#     current_adder = {}
#     pz = 0
#     while current_adder_size <= full_adder_size:
#         x, y, z = "x" + pad_zero(current_adder_size), "y" + pad_zero(current_adder_size), "z" + pad_zero(current_adder_size)
#         gate_dict[nx], gate_dict[ny] =



def main():
    gate_dict = get_input("test_files/prob24_full_input.txt")
    part1(gate_dict)
    # part2(gate_dict)


if __name__ == "__main__":
    main()
