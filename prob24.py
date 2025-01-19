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

    def weak_eq(self, other_operand1, other_operator, other_operand2):
        if {self.operand1, self.operand2} == {other_operand1, other_operand2} and (self.operator == other_operator):
            return True
        return False


def calculate(gate, gate_dict):
    if gate.value:
        return gate.value
    else:
        if gate.operator == "AND":
            gate.value = calculate(gate_dict[gate.operand1], gate_dict) and calculate(gate_dict[gate.operand2], gate_dict)
        elif gate.operator == "OR":
            gate.value = calculate(gate_dict[gate.operand1], gate_dict) or calculate(gate_dict[gate.operand2], gate_dict)
        elif gate.operator == "XOR":
            gate.value = calculate(gate_dict[gate.operand1], gate_dict) ^ calculate(gate_dict[gate.operand2], gate_dict)
        return gate.value


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
            z_values.append((gate_id, calculate(gate_dict[gate_id], gate_dict)))
    z_values = sorted(z_values)
    binary = ""
    for _, val in z_values:
        binary = str(val) + binary
    decimal_out = int(binary, 2)
    print(f"Solution to part 1 is {decimal_out}")


def pad_zero(num):
    num = str(num)
    return "0" + num if len(num) == 1 else num


def walk_backwards(terminal_id, gate_dict, stop_id=None):
    sub_gate_dict = {}
    leaves = [gate_dict[terminal_id]]
    i = 0
    while len(leaves) > 0:
        new_leaves = []
        for leaf in leaves:
            sub_gate_dict[leaf.gate_id] = leaf
            if leaf.gate_id != stop_id:
                if leaf.operand1:
                    new_leaves.append(gate_dict[leaf.operand1])
                if leaf.operand2:
                    new_leaves.append(gate_dict[leaf.operand2])
        leaves = new_leaves
        i += 1
        if i == 1000:
            raise Exception("infinite loop!")
    return sub_gate_dict


def get_gate(gate_dict, new_keys, operand1, operator, operand2):
    matched_gate = next(gate for gate in gate_dict.values() if
                gate.weak_eq(operand1, operator, operand2))
    if matched_gate.gate_id not in new_keys:
        raise ValueError(f"{matched_gate} not in the new keys!")
    return matched_gate


def validate(gate_dict):
    for i in range(2, 45):
        print(i)
        previous_terminal = "z" + pad_zero(i - 1)
        px, py = "x" + pad_zero(i - 1), "y" + pad_zero(i - 1)
        x, y = "x" + pad_zero(i), "y" + pad_zero(i)
        terminal = "z" + pad_zero(i)
        previous_backwards_dict = walk_backwards(previous_terminal, gate_dict)
        backwards_dict = walk_backwards(terminal, gate_dict)
        # assert len(backwards_dict.keys() - previous_backwards_dict.keys()) == 7
        new_keys = backwards_dict.keys() - previous_backwards_dict.keys()
        new_gates = {k: v for k, v in gate_dict.items() if k in new_keys}
        # old_keys = previous_backwards_dict.keys() - backwards_dict.keys()
        # assert old_keys == {previous_terminal}
        previous_terminal_gate = gate_dict[previous_terminal]
        and2 = get_gate(gate_dict, new_keys, px, "AND", py)
        and1 = get_gate(gate_dict, new_keys, previous_terminal_gate.operand1, "AND", previous_terminal_gate.operand2)
        or1 = get_gate(gate_dict, new_keys, and1.gate_id, "OR", and2.gate_id)
        xor1 = get_gate(gate_dict, new_keys, x, "XOR", y)
        xor2 = get_gate(gate_dict, new_keys, or1.gate_id, "XOR", xor1.gate_id)
        assert xor2.gate_id == terminal


def swap_gates(gate_dict, gate1_id, gate2_id):
    new_gate_dict = {}
    for gate_id in gate_dict:
        if gate_id == gate1_id:
            old_gate = gate_dict[gate1_id]
            new_gate_dict[gate2_id] = Gate(operand1=old_gate.operand1, operator=old_gate.operator, operand2=old_gate.operand2, gate_id=gate2_id)
        elif gate_id == gate2_id:
            old_gate = gate_dict[gate2_id]
            new_gate_dict[gate1_id] = Gate(operand1=old_gate.operand1, operator=old_gate.operator,
                                           operand2=old_gate.operand2, gate_id=gate1_id)
        else:
            new_gate_dict[gate_id] = gate_dict[gate_id]
    return new_gate_dict


def try_swapping_gates(gate_dict, fixed_gate):
    for gate in gate_dict:
        swapped_gate_dict = swap_gates(gate_dict, fixed_gate, gate)
        worked = True
        # print(gate)
        try:
            validate(swapped_gate_dict)
        except Exception as e:
            # print(e)
            worked = False
        if worked:
            print(gate)
            break


def part2(gate_dict):
    # This solution is really messy, but the basic idea is to run the `validate` function on the gate_dict.
    # This should give a clue to which gates to swap.  Swap the gates using `swap_gates` and repeat 4 times.
    # Gate ids are redacted here because
    # validate(gate_dict)
    # Swap a <-> b
    gate_dict = swap_gates(gate_dict, "a", "b")
    # validate(gate_dict)
    # Swap c <-> d
    gate_dict = swap_gates(gate_dict, "c", "d")
    # validate(gate_dict)
    # Swap e <-> f
    gate_dict = swap_gates(gate_dict, "e", "f")
    # validate(gate_dict)
    # swap g <-> h
    gate_dict = swap_gates(gate_dict, "g", "h")
    # validate(gate_dict)
    solution = ",".join(list(sorted(["a", "b", "c", "d", "e", "f", "g", "h"])))
    print(solution)


def main():
    gate_dict = get_input("test_files/prob24_full_input.txt")
    part1(gate_dict)
    part2(gate_dict)



if __name__ == "__main__":
    main()
